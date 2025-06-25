Steps to set up the pid_db database with the pid sequence and nextval() function in MariaDB:

1. Create the pid_db Database:

```bash
CREATE DATABASE IF NOT EXISTS pid_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;
```

2. Select the Database:

```bash
USE pid_db
```

3. Create the pid Sequence:

```bash
CREATE SEQUENCE pid
  START WITH 1
  INCREMENT BY 1
  MINVALUE 1
  CACHE 1;
```

4. Create the nextval() Function:

MariaDB uses DELIMITER to allow complex statements. Run the following exactly as shown:

```bash
DELIMITER $$

CREATE FUNCTION nextval(dummy TEXT) RETURNS BIGINT
DETERMINISTIC
MODIFIES SQL DATA
BEGIN
    RETURN NEXT VALUE FOR pid;
END $$

DELIMITER ;
```

The function returns the next integer from the pid sequence each time it's called.

This setup actually does not create any rows in pid table instead it always stores the last value, whenever it is called it returns the stored value and update itself by increasing by 1.
