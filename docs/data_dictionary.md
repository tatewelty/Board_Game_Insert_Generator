# Data Dictionary

Examle numbers are reasonable values if using `mm` as unit.
## Global Parameters

| Field | Type | Description | Example |
|-----|-----|-----|-----|
|`Units:`| dropdown | Unit of measurement: (`mm`, `cm`, `in`)| `mm`|
|`Min Distance To Box Wall:`| number | The minimum distance between a component/cutout and any box wall | `8` |
|`Min Distance Between Cutouts:`| number |The minimum distance between a component/cutout and another component/cutout | `10` |
|`Additional Component Buffer:`| number | Additional amount added to each component's/cutout's length and width | `2` |
|`Circle Resolution (bigger better):`| number | Number of verticies per 1/4 circle.  Higher number makes a smoother circle | `64` |

## Box Parameters
| Field | Type | Description | Example |
|-----|-----|-----|-----|
|`Box Length:`| number | The length of the box in `Units` | `304.8`|
|`Box Width:`| number | The width of the box in `Units` | `304.8` |
|`Box Height:`| number | The height of the box in `Units` | `152.4` |

## Components
Add component button.  Adds a component of type `Rectangular Prism`, `Cylinder`, or `Triangular Prism`

### Rectangular Prism
| Field | Type | Description | Example |
|-----|-----|-----|-----|
|`Length:`| number | The 2D length of component/cutout `Additional Component Buffer is added to this` | `57.15`|
|`Width:`| number | The 2D width of component/cutout `Additional Component Buffer is added to this` | `50.8` |
|`Height:`| number | The 3D height of component/cutout | `10` |

### Cylinder
| Field | Type | Description | Example |
|-----|-----|-----|-----|
|`Radius:`| number | The 2D radius of component/cutout `(Additional Component Buffer/2) is added to this` | `6`|
|`Height:`| number | The 3D height of component/cutout | `10` |

### Triangular Prism
| Field | Type | Description | Example |
|-----|-----|-----|-----|
|`Side 1:`| number | The 2D length of a line of component/cutout `Additional Component Buffer is added to this` | `12`|
|`Side 2:`| number | The 2D length of a line of component/cutout `Additional Component Buffer is added to this` | `13`|
|`Side 3:`| number | The 2D length of a line of component/cutout `Additional Component Buffer is added to this` | `15`|
|`Height:`| number | The 3D height of component/cutout | `10` |
