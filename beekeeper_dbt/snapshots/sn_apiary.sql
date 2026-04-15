{% snapshot sn_apiary %}

{{
    config(
        unique_key='apiary_id',
        strategy='check',
        check_cols=['location_id', 'amount_units']
    )
}}

select * from {{ ref('stg_apiary') }}

{% endsnapshot %}