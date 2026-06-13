select
    product_id,
    product_category_name,
    product_name_lenght::numeric as product_name_length,
    product_description_lenght::numeric as product_description_length,
    product_photos_qty::numeric as product_photos_qty,
    product_weight_g::numeric as product_weight_g,
    product_length_cm::numeric as product_length_cm,
    product_height_cm::numeric as product_height_cm,
    product_width_cm::numeric as product_width_cm
from {{ source('bronze', 'products') }}
