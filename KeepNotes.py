import gkeepapi
import keyring

username = 'ritikparihar6429@gmail.com'
password = 'wdvxkeeezpnsoghw'
master_token = 'aas_et/AKppINbg7OvBu_DNxg47xahBMNovxLAozQnnTAjMuDQwgfiYI0c_RL67ry1v8YM5YuxdKNCXRT8_VY8JCCOjUevR-pCxEaT7oVs8P5ACm-7K9uf1kmKjpQyrtWoSV95twO8uN7YgjFLwkNvlGU1RMu1JUH7v7z3LP1ZtpLIy2DbRB77yQ-iR_LDLLXCpTgnjdZ5orrt9kf9cePtZExtTNqA='

keep = gkeepapi.Keep()
# def __init__():
keep.resume(username, master_token)

def create_note(title, text):
    # keep.sync()
    # keep.resume(username, master_token)
    note = keep.createNote(title, text)
    keep.sync()
    return note

def edit_note(id, text):
    # keep.sync()
    # keep.resume(username, master_token)
    note = keep.get(id)
    note.text = text
    # keep.sync()
    return note

def get_note(id):
    keep.sync()
    # keep.resume(username, master_token)
    return keep.get(id)

def clear_note(id):
    # keep.sync()
    keep.resume(username, master_token)
    note = keep.get(id)
    note.text = ""
    # keep.sync()

# keep = gkeepapi.Keep()
# # sucess = keep.login(username, password)
# # token = keep.getMasterToken()
# # keyring.set_password('google-keep-token', username, token)

# # token = keyring.get_password('google-keep-token', username)
# keep.resume(username, master_token)
# # print(token)

# # print(sucess)
# # note = keep.createNote('tislsa', "Hellofnjas")
# # note.pinned = True
# # note.color = gkeepapi.node.ColorValue.Green
# # keep.sync()

# gnote = keep.get('1LVriOqWt_T5pLmIvko9hfJTlRXfX1qRcb7fCuefQCeU2gQ2g_lPWR_x7g0LMR_ECt6Zb')
# print(gnote.text, " ", gnote.title)
# keep.sync()