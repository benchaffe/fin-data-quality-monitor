select distinct cik, entity_name
from {{ ref('stg_facts') }}
