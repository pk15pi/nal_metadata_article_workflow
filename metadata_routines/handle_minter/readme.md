# handle_minter Subpackage Documentation

The `handle_minter` subpackage provides tools for minting persistent handles and notifying submitters when their articles have been minted handles. It includes two modules: handle_client and mint_and_notify. The `handle_client` module provides an iterface for interacting with the handle database and server. It provides functions for checking if a given handle exists, checking if a given landing page exists, and minting a handle given a pid and a landing page. The `mint_and_notify` module mints handles using the `handle_client` module a sends email notifications to submitters.

---

## Table of Contents

- [Overview](#overview)
- [Configuration](#configuration)
  - [Config File Structure](#config-file-structure)
  - [Environment Variable](#environment-variable)
- [handle_client Module](#handle_client-module)
  - [Usage](#usage-handle_client)
- [mint_and_notify Module](#mint_and_notify-module)
  - [Usage](#usage-mint_and_notify)

---

## Overview

The `handle_minter` subpackage is designed to:
- Mint new handles for records using the Handle System.
- Check for existing records in Alma.
- Notify submitters or developers via email when a record is published.

---

## Configuration

### Config File Structure

The subpackage requires a TOML configuration file. Below is an example (`sample_config.toml`):

```toml
[email_notification]
smtp_server = 'mailproxy1.usda.gov'
send_from = 'nal-pubag-curator@usda.gov'
bcc = ''
subject = "Manuscript Submission Published"
body_template = """

Dear {},

Your submission for the article titled "{}" is now available in PubAg.

The agid for your article is: {}

You can access the article using the following link: https://handle.nal.usda.gov/{}

Sincerely,
PubAg Curator

USDA National Agricultural Library
"""

[debug]
testing_mode = 0
handle_service_conn = 1
email_submitter = 1
email_dev = 0
dev_address = 'dev@example.com'
```

**Descriptions:**
- `[email_notification]`: Email settings and templates.
  - `smtp_server`: SMTP server for sending emails.
  - `send_from`: Email address from which notifications are sent.
  - `bcc`: BCC email address (optional).
  - `subject`: Subject line for the email.
  - `body_template`: Template for the email body, with placeholders for recipient name, title, agid, and handle.
- `[debug]`: Debug and testing flags.
- `testing_mode`: If set to `1`, the module will run in testing mode, and will not connect to the pid database, the handle database, or the handle service. The handle_client module will return canned responses instead of actually connecting to the databases or services.
  - `handle_service_conn`: If set to `1`, the handle service connection is enabled. If set to `0`, instead of actually connecting to the handle service, it will print debug messages.
  - `email_submitter`: If set to `1`, emails will be sent to the submitter. If set to `0`, no emails will be sent to the submitter.
  - `email_dev`: If set to `1`, AND if `email_submitter` is set to `0`, emails will be sent to the developer. If both `email_submitter` and `email_dev` are set to `0`, no emails will be sent and a debug message will be printed instead.
  - `dev_address`: Email address for the developer (used when `email_dev` is set to `1`).

### Environment Variables

Set the `HANDLE_MINTER_CONFIG` environment variable to the path of your config file.  
Example:
```sh
export HANDLE_MINTER_CONFIG=/path/to/sample_config.toml
```
Set the following environment variables to connect to the PID database. This documentation uses sample values. Ensure you replace them with your actual database connection details.
```sh
export PID_DB_NAME='pid_db_name'
export PID_DB_USER='pid_db_user'
export PID_DB_PASSWORD='pid_db_password'
export PID_DB_HOST='pid_db_host'
export PID_DB_PORT='pid_db_port'
```
Set the following environment variables to connect to the handle database and handle service. This documentation uses sample values. Ensure you replace them with your actual connection details.
```sh
export HANDLE_DB_NAME='handle_db_name'
export HANDLE_DB_USER='handle_db_user'
export HANDLE_DB_PASSWORD='handle_db_password'
export HANDLE_DB_HOST='handle_db_host'
export HANDLE_DB_PORT='handle_db_port'
export HANDLE_SERVICE_URL='https://handle.service.url'
```
Finally, set the following environment variable to the file path for the json file containing the headers needed for the handle service connection.
```sh
export HANDLE_API_HEADERS='/path/to/headers.json'
```

---

## The `handle_client` Module

The `handle_client` module provides a `HandleClient` class for interacting with the Handle System.

### Usage {#usage-handle_client}

1. **Instantiate the client:**
   ```python
   from handle_minter.handle_client import HandleClient

   hc = HandleClient()
   ```

2. **Check if a handle exists:**
   ```python
   handle_exists = hc.check_handle_exists('10113/test-0000')
   print(handle_exists)
   ```

3. **Check if a landing page exists:**
   ```python
   landing_page_exists = hc.check_landing_page_exists('https://example.com/landing_page')
    print(landing_page_exists)
   ```

4. **Create a new handle with a pid and a landing page:**
   ```python
   result = hc.create_handle('test-0000', 'https://example.com/landing_page')
   if result:
       print(f"New handle minted: {result}")
   else:
       print("Handle creation failed.")
   ```
**Note:**
Testing mode is enabled by passing `testing_mode=True` to the HandleClient() object. This is only necessary for the unit tests. In production, the `testing_mode` parameter can be omitted, as it is set to `False` by default. When in testing mode, the `check_handle_exists` and `check_landing_page_exists` functions will always return `False`. 
---

## The `mint_and_notify` Module

The `mint_and_notify` module provides the `mint_and_notify` function, which:
- Receives a dictionary including the pid, mmsid, provider_rec, title, submitter_email, and submitter_name.
- Checks for existing records in Alma with the given mmsid. If the record does not yet exist in Alma, the `mint_and_notify` function returns a result of 'not found in Alma' and does not mint a handle.
- Checks if the handle already exists. If it does not yet exist, it mints a new handle using the `HandleClient` class.
- Notifies the submitter or developer via email.

### Usage {#usage-mint_and_notify}

1. **Prepare the input data:**
   ```python
   handle_data = {
       'pid': 'test-0000',
       'mmsid': '000000000001',
       'provider_rec': '1234',
       'title': 'Super important article',
       'submitter_email': 'user@example.com',
       'submitter_name': 'Jane Doe'
   }
   ```

2. **Call the function:**
   ```python
   from handle_minter.mint_and_notify import mint_and_notify

   result, message = mint_and_notify(handle_data)
   print(f"Process result: {result}, message: {message}")
   ```

## Additional Notes

- Ensure all dependencies are installed (see `requirements.txt`).
- For production, set `handle_service_conn` and `email_submitter` to `1` in the config.
- The `mint_and_notify` function expects all required fields in the `handle_data` dictionary.

---