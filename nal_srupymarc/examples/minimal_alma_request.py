import srupymarc

query = 'alma.mms_id=9915695874407426'
params = {
    "url": "https://na91.alma.exlibrisgroup.com/view/sru/01NAL_INST",
    "query": query
}
response = srupymarc.searchretrieve(**params)
