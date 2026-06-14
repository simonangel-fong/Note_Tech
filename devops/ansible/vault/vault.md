# Ansible - Vault

[Back](../ansible.md)

- [Ansible - Vault](#ansible---vault)
  - [Vault](#vault)
  - [Lab: encrypt a string](#lab-encrypt-a-string)
  - [Lab: encrypt and decrypt file](#lab-encrypt-and-decrypt-file)

---

## Vault

- `Ansible Vault`
  - used to encrypt sensitive data within the infrastructure automation files.
  - uses AES256 encryption to secure this data, allowing to safely **store the secrets in version control** (like Git) without exposing them in plain text.

| CMD                                                            | DESC                                                                                  |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `ansible-vault --version`                                      | Show installed version.                                                               |
| `ansible-vault create secrets.yml`                             | Create a new encrypted file. Ansible asks for a vault password, then opens an editor. |
| `ansible-vault view secrets.yml`                               | View an encrypted file without editing it.                                            |
| `ansible-vault edit secrets.yml`                               | Open and edit an encrypted file.                                                      |
| `ansible-vault encrypt secrets.yml`                            | Encrypt an existing plaintext file.                                                   |
| `ansible-vault decrypt secrets.yml`                            | Decrypt an encrypted file back to plaintext.                                          |
| `ansible-vault rekey secrets.yml`                              | Change the vault password for an encrypted file.                                      |
| `ansible-vault encrypt_string --prompt --name 'variable_name'` | converts a plain-text secret into a secure, encrypted YAML block                      |

---

## Lab: encrypt a string

```sh
# fails due to no sudo pwd
ansible ubuntu -m ping -o
# ubuntu2 | FAILED! => {"msg": "Missing sudo password"}
# ubuntu1 | FAILED! => {"msg": "Missing sudo password"}
# ubuntu3 | FAILED! => {"msg": "Missing sudo password"}

# encrypt the "pasword" as the key "ansible_become_pass"; and ask for pass to encrypt
ansible-vault encrypt_string --name 'ansible_become_pass' 'password' --ask-vault-pass
# New Vault password:
# Confirm New Vault password:
# Encryption successful
# ansible_become_pass: !vault |
#           $ANSIBLE_VAULT;1.1;AES256
#           32643131653737643866316664356662333330323639633163643931343562373530363034653538
#           3865303534623139643231313762356665386130313134330a633062633835336630393763316166
#           61373362306262373439346334633666393538346134346365613063363365393530376637383962
#           6434663936313130620a613965636631343131623233356330623962343231333463616364316265
#           6439

# add vault in group_vars
tee group_vars/ubuntu<<EOF
ansible_become: true
ansible_become_pass: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          32643131653737643866316664356662333330323639633163643931343562373530363034653538
          3865303534623139643231313762356665386130313134330a633062633835336630393763316166
          61373362306262373439346334633666393538346134346365613063363365393530376637383962
          6434663936313130620a613965636631343131623233356330623962343231333463616364316265
          6439
EOF

# ping and ask for vault pass to decript
ansible --ask-vault-pass ubuntu -m ping -o
# ubuntu1 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# ubuntu2 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# ubuntu3 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
```

---

## Lab: encrypt and decrypt file

- encrypt file

```sh
tee external_vault_vars.yaml<<EOF
external_vault_var: Example External Vault Var
EOF

ansible-vault encrypt external_vault_vars.yaml
# New Vault password:
# Confirm New Vault password:
# Encryption successful

cat external_vault_vars.yaml
# $ANSIBLE_VAULT;1.1;AES256
# 61333435343931306633653962353033386532653165613466363835336264653732626530303563
# 6537323864326239633837323833346662323836373163650a383732323664646436356164613938
# 34393232613465613032313763653737353235363337643937646233376366616437643038636530
# 6337333065333037640a613638623831393139313363356132633366306165383663653730343430
# 65393439636232346137363738323864616363663361346266343738396432366432323164643964
# 3861656336663434383432613966353366333164336337346161

tee demo_vault_var_file.yaml<<EOF
- hosts: ubuntu
  vars_files:
     - external_vault_vars.yaml

  tasks:
    - name: Show external_vault_var
      debug:
        var: external_vault_var
EOF

ansible-playbook --ask-vault-pass demo_vault_var_file.yaml
ansible-playbook --ask-vault-pass demo_vault_var_file.yaml
Vault password:
# PLAY [ubuntu] ***********************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu3]
# ok: [ubuntu2]
# ok: [ubuntu1]

# TASK [Show external_vault_var] ******************************************************************************************************
# ok: [ubuntu1] => {
#     "external_vault_var": "Example External Vault Var"
# }
# ok: [ubuntu2] => {
#     "external_vault_var": "Example External Vault Var"
# }
# ok: [ubuntu3] => {
#     "external_vault_var": "Example External Vault Var"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

- decrypt file

```sh
ansible-vault decrypt external_vault_vars.yaml
# Vault password:
# Decryption successful

cat external_vault_vars.yaml
# external_vault_var: Example External Vault Var
```

- re-key: decrypt and re-encrypt

```sh
# encrypt
ansible-vault encrypt external_vault_vars.yaml
# New Vault password:
# Confirm New Vault password:
# Encryption successful

# rekey
ansible-vault rekey external_vault_vars.yaml
# Vault password:
# New Vault password:
# Confirm New Vault password:
# Rekey successful
```

- View the encrypt value file

```sh
ansible-vault view external_vault_vars.yaml
# Vault password:
# external_vault_var: Example External Vault Var
```

- encrypt value file with a password files

```sh
echo password > pwd_file

ansible-vault view external_vault_vars.yaml --vault-password-file pwd_file
# external_vault_var: Example External Vault Var
```

- using vault-id

```sh
# with prompting pwd
ansible-vault view --vault-id @prompt external_vault_vars.yaml
# Vault password (default):
# external_vault_var: Example External Vault Var

ansible-vault view --vault-id @pwd_file external_vault_vars.yaml
# external_vault_var: Example External Vault Var
```

- Using vault-id

```sh
# decrypt
ansible-vault decrypt external_vault_vars.yaml
# Vault password:
# Decryption successful

# encrypt var file with id vars
ansible-vault encrypt --vault-id vars@prompt external_vault_vars.yaml
# New vault password (vars):
# Confirm new vault password (vars):
# Encryption successful

cat external_vault_vars.yaml
# $ANSIBLE_VAULT;1.2;AES256;vars
# 34613739633665633030356131376463643438633138366333613361613234376463623838313565
# 3037636165343832306262653131346163616131316535620a386131656339333564393731356633
# 35333637353439323631363361656231653863366138326362323066353937313639333137396464
# 3639393433666337310a666162653938616262663666306636306166333934633939636331646562
# 32633933353239653765336233323865323632326634366433393533363463626536326331333139
# 6438353237366362373439616634316137313033623330303730

# encrypt ssh with ssh vars
ansible-vault encrypt_string --vault-id ssh@prompt --name 'ansible_become_pass' 'password'
# New vault password (ssh):
# Confirm new vault password (ssh):
# Encryption successful
# ansible_become_pass: !vault |
#           $ANSIBLE_VAULT;1.2;AES256;ssh
#           31336335653266636335613861623663633063356231363065333439653539386235613131306534
#           3631386366316636396137626238356533373936396530390a313931353931396537343964333732
#           66396435356236653339643936343463343731393562323832646336643365316266643139646532
#           6562363233623738610a343234306639613239393732363630393435386337613063343735316531
#           3732

tee group_vars/ubuntu <<'EOF'
ansible_become: true
ansible_become_pass: !vault |
          $ANSIBLE_VAULT;1.2;AES256;ssh
          31336335653266636335613861623663633063356231363065333439653539386235613131306534
          3631386366316636396137626238356533373936396530390a313931353931396537343964333732
          66396435356236653339643936343463343731393562323832646336643365316266643139646532
          6562363233623738610a343234306639613239393732363630393435386337613063343735316531
          3732
EOF

ansible ubuntu --vault-id ssh@prompt -m ping -o




# test connect with vault id ssh
ansible ubuntu --vault-id ssh@prompt -m ping -o
# Vault password (ssh):
# ubuntu1 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# ubuntu2 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}
# ubuntu3 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3.10"},"changed": false,"ping": "pong"}

# execute with 2 vault id
ansible-playbook --vault-id vars@prompt --vault-id ssh@prompt demo_vault_var_file.yaml
# Vault password (vars):
# Vault password (ssh):

# PLAY [ubuntu] ***********************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu1]
# ok: [ubuntu3]
# ok: [ubuntu2]

# TASK [Show external_vault_var] ******************************************************************************************************
# ok: [ubuntu1] => {
#     "external_vault_var": "Example External Vault Var"
# }
# ok: [ubuntu2] => {
#     "external_vault_var": "Example External Vault Var"
# }
# ok: [ubuntu3] => {
#     "external_vault_var": "Example External Vault Var"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

- encript entire playbook

```sh
ansible-vault encrypt --vault-id playbook@prompt demo_vault_var_file.yaml
# New vault password (playbook):
# Confirm new vault password (playbook):
# Encryption successfu

cat demo_vault_var_file.yaml
# $ANSIBLE_VAULT;1.2;AES256;playbook
# 65356261383335626533323039343433623639633862396535383464653661616362383861333732
# 3839336635386131353936346438393864643065336163630a303164616366623734396565663565
# 32353861633465636333383961303361313734316433353361356132336361643433386438346261
# 3161663837393362380a393332393330653134616666323261646262633734323739646337333935
# 35663862626430663331643366363232326334346434623765653631316666633630643431373836
# 66313264383035396432636634336334373363316232383030343437393566396461333464336132
# 30343631383237616638383265386463666230323830636634343362653437613862643937656134
# 34383830646138633234666632373566636334316137346231653762633731396636333534343037
# 61316132393964393564623438316465303463653334623834633165353965383933323234623335
# 61366434326633646265386630616665656534616137623964326334363935366430316130643166
# 61333336333136663236643663653333363363383362333235633435376432376466663861343139
# 38393264613439366264

ansible-vault view --vault-id playbook@prompt demo_vault_var_file.yaml
# - hosts: ubuntu
#   vars_files:
#      - external_vault_vars.yaml

#   tasks:
#     - name: Show external_vault_var
#       debug:
#         var: external_vault_var

# execute
ansible-playbook --vault-id vars@prompt --vault-id ssh@prompt --vault-id playbook@prompt demo_vault_var_file.yaml
# Vault password (vars):
# Vault password (ssh):
# Vault password (playbook):

# PLAY [ubuntu] ***********************************************************************************************************************

# TASK [Gathering Facts] **************************************************************************************************************
# ok: [ubuntu2]
# ok: [ubuntu1]
# ok: [ubuntu3]

# TASK [Show external_vault_var] ******************************************************************************************************
# ok: [ubuntu1] => {
#     "external_vault_var": "Example External Vault Var"
# }
# ok: [ubuntu2] => {
#     "external_vault_var": "Example External Vault Var"
# }
# ok: [ubuntu3] => {
#     "external_vault_var": "Example External Vault Var"
# }

# PLAY RECAP **************************************************************************************************************************
# ubuntu1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
# ubuntu3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```