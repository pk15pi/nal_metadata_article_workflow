from handle_minter.mint_and_notify import mint_and_notify

# Example 1: Record not found in Alma
handle_data = {
    "pid": "test-2222",
    "submitter_email": "noa.mills@usda.gov",
    "submitter_name": "Your Eternal Legacy",
    "mmsid": "1234",
    "provider_rec": "provider_rec",
    "title": "Super important article"
}

# Should return 'Not in Alma'
result, message = mint_and_notify(handle_data)
print(f"Result: {result}")
print(f"Message: {message}")