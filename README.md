# statsdelta - statistics delta

statsdelta is a commandline command (Python3 program) that compares two (CSV) statistics with each other and generates delta values from the (old and the new) values.

## Usage

```
statsdelta

required arguments:
  -from FROM_FILE                      The file to use as the left or from source for the delta calculation (default: None)
  -to TO_FILE                          The file to use as the right or to source for the delta calculation (default: None)
  -key-field KEY_FIELD                 The key field name (column name) (default: None)

optional arguments:
  -h, --help                           show this help message and exit
  -delimiter DELIMITER                 The field delimiter used within the file; use TAB for tab-delimited (default: ,)
  -output-fields OUTPUT_FIELDS         The names of the fields (column names) to include in the delta output (if this argument is not specified, then the header from the "from" CSV file is taken) (default: None)
```

* example:
    ```
    statsdelta -from [PATH THE FROM CSV FILE] -to [PATH TO THE TO CSV FILE] -key-field [KEY FIELD NAME] > [PATH TO THE OUTPUT CSV FILE]
    ```

## Run

* clone this git repo or just download the [statsdelta.py](statsdelta/statsdelta.py) file
* run ./statsdelta.py
* for a hackish way to use esfstats system-wide, copy to /usr/local/bin

### Install system-wide via pip

```
sudo -H pip3 install --upgrade [ABSOLUTE PATH TO YOUR LOCAL GIT REPOSITORY OF STATSDELTA]
```
(which provides you ```statsdelta``` as a system-wide commandline command)

## Description

### Diff Status

|Diff Status|Description|
|-----------|-----------|
|changed|some values (/statistics; included in this comparison) have been changed for this field (key)|
|not changed|no values (/statistics; included in this comparison) have been changed for this field (key)|
|added|this field (key) has been added to the 'to' statistic|
|deleted|this field (key) has been removed from the 'to' statistic|