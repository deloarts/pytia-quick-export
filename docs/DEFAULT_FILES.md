# default files

Explains the config of all default files.

All default files can be copied, renamed and edited to fit your needs.

## 1 excel.default.json

This file contains the configuration for the final bill of material excel file.

- **Location**: [/pytia_quick_export/resources/excel.default.json](../pytia_quick_export/resources/excel.default.json)
- **Rename to**: `bom.json`

### 1.1 file content

```json
{
    "header_row": 0,
    "data_row": 1,
    "header_items": [
        "pytia.project",
        "pytia.machine",
        "$number",
        "$type",
        "$quantity",
        "$partnumber",
        "$definition",
        "$revision",
        "pytia.material",
        "pytia.base_size",
        "pytia.base_size_preset",
        "pytia.mass",
        "$source",
        "pytia.manufacturer",
        "pytia.supplier",
        "pytia.spare_part_level",
        "pytia.tolerance",
        "pytia.creator",
        "pytia.modifier",
        "$description",
        "pytia.note_general",
        "pytia.note_material",
        "pytia.note_base_size",
        "pytia.note_supplier",
        "pytia.note_production",
        "pytia.process_1",
        "pytia.note_process_1",
        "pytia.process_2",
        "pytia.note_process_2",
        "pytia.process_3",
        "pytia.note_process_3",
        "pytia.process_4",
        "pytia.note_process_4",
        "pytia.process_5",
        "pytia.note_process_5",
        "pytia.process_6",
        "pytia.note_process_6"
    ],
    "font": "Monospac821 BT",
    "size": 8,
    "header_color": "FFFFFF",
    "header_bg_color": "007ACC",
    "data_color_1": "000000",
    "data_bg_color_1": "F0F0F0",
    "data_color_2": "000000",
    "data_bg_color_2": "FFFFFF"
}
```

### 1.2 description

name | type | description
--- | --- | ---
header_row | `int` | The row number which shows the header. This value is zero-indexed, add `1` to match the row in Excel.
data_row | `int` | The row number from which the data will be written. This value is zero-indexed, add `1` to match the row in Excel.
header_items | `list` | A list of the header items that will be shown in the final export in the order of this list. These header items represent the properties of the parts and products. User-properties can be added by their name, CATIA properties and special properties must be added with a dollar sign `$` prefix (see keywords.json).
font | `str` | The font of the final bill of material.
size | `int` | The font size of the final bill of material.
header_color | `str` | The header font color of the final bill of material.
header_bg_color | `str` | The header background color of the final bill of material.
data_color_1 | `str` | The font color for each even row of the final bill of material.
data_bg_color_1 | `str` | The background color for each even row of the final bill of material.
data_color_2 | `str` | The font color for each odd row of the final bill of material.
data_bg_color_2 | `str` | The background color for each odd row of the final bill of material.

## 2 properties.default.json

This file contains all part/product properties, which are required for this app.

- **Location**: [/pytia_quick_export/resources/properties.default.json](../pytia_quick_export/resources/properties.default.json)
- **Rename to**: `properties.json`

### 2.1 file content

```json
{
    "project": "pytia.project",
    "machine": "pytia.machine",
    "creator": "pytia.creator",
    "modifier": "pytia.modifier"
}
```

### 2.2 description

name | type | description
--- | --- | ---
`generic` | `str` | The name of the property, which stores the value of `generic`.
