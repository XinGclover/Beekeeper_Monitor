with user as (
    select *
    from {{ ref('stg_user') }}
),
role as (
    select *
    from {{ ref('stg_role') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['user_id']) }} as user_key,
    u.user_id,
    u.user_name,
    u.email,
    u.notifications_enabled,
    r.role_name as role,
    CURRENT_TIMESTAMP AS valid_from,
    TIMESTAMP '9999-12-31 00:00:00' AS valid_to,
    TRUE AS is_current
from user u
left join role r on u.role_id = r.role_id