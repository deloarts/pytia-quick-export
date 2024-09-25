# default files

Explains the config of all default files.

All default files can be copied, renamed and edited to fit your needs.

## 1 excel.default.json

This file contains the configuration for the final bill of material excel file.

- **Location**: [/pytia_quick_export/resources/excel.default.json](../pytia_quick_export/resources/excel.default.json)
- **Rename to**: `excel.json`

### 1.1 file content

```json
{
    "header_row": 0,
    "data_row": 1,
    "header_items_made": [
        "Project:pytia.project",
        "Product:pytia.product",
        "Number:$number",
        "Type:$type",
        "Quantity:$quantity",
        "Unit=PCS",
        "Partnumber:$partnumber",
        "Definition:$definition",
        "Rev:$revision",
        "Material:pytia.material",
        "Base Size:pytia.base_size",
        "Base Size Preset:pytia.base_size_preset",
        "Mass:pytia.mass",
        "Order Number:pytia.order_number",
        "Manufacturer:pytia.manufacturer",
        "Supplier:pytia.supplier",
        "SPL:pytia.spare_part_level",
        "Tolerance:pytia.tolerance",
        "Creator:pytia.creator",
        "Modifier:pytia.modifier",
        "Description:$description",
        "Note:pytia.note_general",
        "Note Material:pytia.note_material",
        "Note Base Size:pytia.note_base_size",
        "Note Supplier:pytia.note_supplier",
        "Note Production:pytia.note_production",
        "Process 1:pytia.process_1",
        "Note Process 1:pytia.note_process_1",
        "Process 2:pytia.process_2",
        "Note Process 2:pytia.note_process_2",
        "Process 3:pytia.process_3",
        "Note Process 3:pytia.note_process_3",
        "Process 4:pytia.process_4",
        "Note Process 4:pytia.note_process_4",
        "Process 5:pytia.process_5",
        "Note Process 5:pytia.note_process_5",
        "Process 6:pytia.process_6",
        "Note Process 6:pytia.note_process_6"
    ],
    "header_items_bought": [
        "Project:pytia.project",
        "Product:pytia.product",
        "Number:$number",
        "Type:$type",
        "Quantity:$quantity",
        "Unit=PCS",
        "Partnumber:$partnumber",
        "Definition:$definition",
        "Rev:$revision",
        "Mass:pytia.mass",
        "Order Number:pytia.order_number",
        "Manufacturer:pytia.manufacturer",
        "Supplier:pytia.supplier",
        "SPL:pytia.spare_part_level",
        "Creator:pytia.creator",
        "Modifier:pytia.modifier",
        "Description:$description",
        "Supplier:pytia.note_supplier"
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
header_items_made | `list` | A list of the header items for the made item that will be shown in the final export as worksheet in the order of this list. These header items must be defined with the following syntax: `HEADER NAME:PROPERTY NAME` or `HEADER NAME=FIXED TEXT`<br><ul><li>User-properties can be added by their name. E.g.: If you want the project number to have the header name "Project", you have to write the value as `Project:pytia.project` (assuming that the project number is stores as 'pytia.project' in the document's properties).</li><li>CATIA properties and special properties must be added with a dollar sign `$` prefix (see keywords.json). E.g.: To add the partnumber you have to write it like this: `Part Number:$partnumber`. This creates the column **Part Number**.</li><li>Further it is possible to apply *fixed text*. This is done with header name followed by the equal sign `=` and then followed by the value of that fixed text. E.g: If you want a column **Unit** with the text **Pcs** in every item of the bom, you have to add `"Unit=Pcs"` to the header_items list.</li><li>An item that has neither a double point `:`, not an equal sign `=` in it will represent an empty row, with the value as header name.</li></ul>
header_items_bought | `list` | Same as header_items_made, but for documents with the source `bought`. If you don't need to separate between made and bought, just leave both lists with the same items.
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
    "product": "pytia.product",
    "creator": "pytia.creator",
    "modifier": "pytia.modifier"
}
```

### 2.2 description

name | type | description
--- | --- | ---
`generic` | `str` | The name of the property, which stores the value of `generic`.
