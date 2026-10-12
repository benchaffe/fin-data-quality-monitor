with latest_run as (
    select *
    from {{ ref('stg_facts') }}
    where run_id = (select max(run_id) from {{ source('raw', 'loads') }})
      and form in ('10-K', '10-K/A', '10-Q', '10-Q/A')
),
ranked as (
    select
        f.cik, m.metric, f.period_start, f.period_end,
        f.fiscal_year, f.fiscal_period, f.form, f.filed_date, f.accession, f.value,
        row_number() over (
            partition by f.cik, m.metric, f.period_start, f.period_end
            order by m.priority asc, f.filed_date desc, f.accession desc
        ) as rn
    from latest_run f
    join {{ ref('dim_metric') }} m on f.tag = m.tag
)
select cik, metric, period_start, period_end, fiscal_year, fiscal_period,
       form, filed_date, accession, value
from ranked
where rn = 1