{% snapshot sn_hive %}

{{
    config(
        unique_key='hive_id',
        strategy='check',
        check_cols=['apiary_id', 'hive_type_id']
    )
}}

select * from {{ ref('stg_hive') }}

{% endsnapshot %}