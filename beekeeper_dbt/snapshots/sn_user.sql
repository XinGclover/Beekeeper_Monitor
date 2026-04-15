{% snapshot sn_user %}

{{
    config(
        unique_key='user_id',
        strategy='check',
        check_cols=['user_name', 'email', 'notifications_enabled', 'role_id']
    )
}}

select * from {{ ref('stg_user') }}

{% endsnapshot %}