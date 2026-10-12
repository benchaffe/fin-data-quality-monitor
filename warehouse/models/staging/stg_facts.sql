select *
from {{ source('raw', 'raw_facts') }}
where unit = 'USD'