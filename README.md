# Fuzzy-Matcher
Fuzzy Match a name with a standard list

## Components

The module is broadely divided into three main parts :-
1. Validator
2. Matcher
3. Updater

### Valdiator

Valdiation is done via specifying a schema as json.
The parent file is `main-schema.json`. As of the first release, we are pushing currency and university name validations.
The specific schema requirements are specified in their own schema files, `currencies.json` and `universities.json` respectively.

#### So, what does the Validator do ?

The Validator performs a simple sanity check on the data entered and returns the non-conformant data. In layman terms, the validator performs a sort of simple string comparison over the requested entities. The entries which are not exactly matched or are in an unconventional format, example, a digit in university name or a four letter currency ISO code, are identified here. This sets the stage for our Fuzzy-Matcher.

### Matcher

Matcher uses the `fuzzywuzzy` library. It computes the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance#:~:text=Informally%2C%20the%20Levenshtein%20distance%20between,considered%20this%20distance%20in%201965.) for   string comparison.

The matcher takes in the non-exact matches as returned by the validator. It then tries to fuzzy match these names against our standard list obtained from [grid.ac](https://grid.ac/downloads).

### Updater

This is a simple script that overwrites the non-conformant entries after the user reviews them. This is run separately since it can run only after the user reviews the suggestions by the matcher.

## Running the modules

1. First, install the dependencies with 

    `pip -r requirements.txt`

2. The file, `driver.py` runs the Validator and Matcher and `updater.py` runs the final update script.

3. The usage is as follows

    `python driver.py <path_to_input_file> <path_to_output_file>`

4. This generates two files -

    - Non-conformant data entries are returned by the validator in a csv named `entries_to_fuzzy_match.csv`.
    - `entries_to_fuzzy_match.csv` is fed to the matcher which outputs `Suggestions.csv`

5. An extra column called `'Correct (1/0)'` is added to `Suggestions.csv` where the user determines which entry to update.
6. This updated `Suggestions.csv` is now read by `updater.py` which updates the originally uploaded data with the standardised entries.
