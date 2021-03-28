
# `better_csv_to_json`
This modestly and cleverly-named tool is used for converting data from .csv files (or any comma delimited file which meets the same specification) to JSON format, and vice-versa.

#### Why would you want to do this?
I've personally found a need for such a tool in the following situations:
1. Making schema-level changes to configuration data is often much easier and faster with a spreadsheet interface vs. editing a .json file which can often have you needing to change objects one at a time. 
2. 

## Specification:
`better_csv_to_json` uses some simple syntax in the column-heading to determine how the resulting JSON data is created and formatted.

If you have simple data and no need for nested objects, values to be represented as arrays, etc. Then there's not much you need to know.
**That said, there is reserved syntax you may want to be aware of**. Most notably, column headings are period delimited to represent object-nesting. **This can be toggled off** by setting the `evaluate_heading_syntax` value to false

### Basics:

* `better_csv_to_json` produces an `array` of objects with each row in the .csv existing as an object in the array. 
    * Unless specified with the `arraykey` string parameter, the name of this array in the JSON will be the same as .csv filename.
        * e.g., `people.csv` becomes an array with the key of `people`.
    


### Heading Syntax:


_______
#### Heading Properties:

* Both keys and values are case ***insensitive***, except default values. 
* Key-Value Pairs are separated by commas.

Below are each of the built-in properties usable inside curly braces which `better_csv_to_json` evaluates (with examples):

* `default`
    * If a row has this column empty, the value is to the right of the equals sign is used.
    * **Examples**: 
      * ExampleHeading: `HomePlanet{default=earth}`
      * ExampleValue: `(empty)`
        ```json
        {
          "homePlanet": "earth" 
        }
        ```    
    
* `type`
    * accepted values: `string`, `num`, `bool`, `literal`
    * Explicitly determines the value that this column will be represented as in JSON.
    * If not explicitly declared, `better_csv_to_json` will infer based on the value in the first row.
    * **Examples**:
      1. 
          * ExampleHeading: `Age` <- The type is not declared, but the value of `10` is interpreted by `better_csv_to_json` as a `num`.
          * ExampleValue: `10`  
            ```json
            {
              "age": 10
            }
            ```
      2.  
          * ExampleHeading: `Age{type=string}` <- This forces the value in the .csv to be converted to that of a `string`
          * ExampleValue: `10`  
            ```json
            {
              "age": "10"
            }
            ```
      3.  
          * ExampleHeading: `Age{type=bool}` <- This obviously doesn't make any sense, but the input value of `10` will still be converted to a `bool`. In this case, it is `true` since the value is greater than `1`.
          * ExampleValue: `10`
            ```json
            {
              "age": true
            }
            ```
      4.  (The `literal` `type` is explained in greater detail in its own section below)
          * ExampleHeading: `favoriteFood{type=literal}`
          * ExampleValue: `"name":tacos,"origin":"mexico"`
            ```json
            {
              "favoriteFood": {
                  "name":"tacos",
                  "origin": "mexico" 
              } 
            }
            ```
* `exclude`
    * accepted values:
        * `always`  : column will be excluded entirely from resulting JSON.
        * `ifEmpty`: column will only be included as part of object if it is not empty. 
    * Setting this property determines if the resulting JSON will include the object represented by the column. If no value for this property is set, the column will always be included in each object.
      * **Examples**:
        1.
           * ExampleHeading: `EmailAddress`,`age`
           * ExampleValue: `(empty)`,`99`
            ```json
              {
                "emailAddress": "",
                "age": 99
              }
            ```  
        2.
        * ExampleHeadings: 'EmailAddress{excludeIfEmpty=true}',`age`
        * ExampleValue: `(empty)`,`99`
            ```json
              {
                //no object created for emailAddress
                "age": 99
              }
            ```  
        
* `preserveCase`
    * accepted values:
        * `true` : if set to true, `better_csv_to_json` will preserve the casing of the value.
        * `false` *(default)*: if set to false, `better_csv_to_json` will convert the values to the casing specified in the conversion parameters.
    
* `ignoreObjectDelimiter`
    * accepted values:
        * `true` : if set to true, `better_csv_to_json` will not evaluate object delimiting and treat the column as a standard one.
        * `false` *(default)*: if set to false, `better_csv_to_json` will convert the value to a JSON Object using the post-delimiter values as the keys for nested values.
    
_______
#### Arrays
The reserved value `[,]` indicates that the values in the column are represented as a comma-delimited array.

For simple arrays

* Place the `[,]` value either at the end of the heading: `FavoriteFoods{type=string}[,]` or in between the heading name and its properties:`FavoriteFoods[,]{type=string}`
* If the `type` property is declared, that is the type that the array values will be represented as.  If it is *not* declared, `better_csv_to_json` will infer type based on the first value in the first row's array.

The above example becomes:
```json
{
  "favoriteFoods": [
    "burgers","pizza","tacos"
  ]
}
```


_______
#### Creating Nested Objects:
Headings with a `.` (period) will be delimited and add their values as a nested value to the specified root object.

**Simple Nesting**:

A heading of `hair.length` with a value of `medium` will result in the following:
```json
{
  "hair": {
    "length": "medium"
  }
}
```

If there are several columns with headings which include the `hair` name as the root, they will be amalgamated into a single `hair` object in the resulting JSON.
For example, if the .csv has the following columns: `Hair.Length`,`Hair.Color`, `Hair.Shininess`, this results in the following:
```json
{
  "hair": {
    "length": "long",
    "color": "brown",
    "shininess": 150
  }
}
```

**Complex Nesting**:

This approach can make spreadsheets become quite complex if overused, but it works 

_______

#### JSON Literals

Using the `type` property in the heading, you can specify that the values in the column will be interpreted as JSON literal values.
