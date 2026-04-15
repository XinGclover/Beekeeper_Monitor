{% snapshot sn_sensor %}

{{
    config(
        unique_key='sensor_id',
        strategy='check',
        check_cols=['hive_id', 'sensor_type_id', 'is_hive_level', 'status']
    )
}}

select * from {{ ref('stg_sensor') }}

{% endsnapshot %}