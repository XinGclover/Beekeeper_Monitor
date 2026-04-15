with seconds as (

    select generate_series(0, 86399) as second_of_day

)

select
    to_char(time '00:00:00' + second_of_day * interval '1 second', 'HH24MISS')::int as time_key,
    (time '00:00:00' + second_of_day * interval '1 second') as full_time,

    extract(hour from time '00:00:00' + second_of_day * interval '1 second')::int as hour,
    extract(minute from time '00:00:00' + second_of_day * interval '1 second')::int as minute,
    extract(second from time '00:00:00' + second_of_day * interval '1 second')::int as second,

    floor(second_of_day / 60)::int as minute_of_day,

    case
        when extract(hour from time '00:00:00' + second_of_day * interval '1 second') between 0 and 5
        then true
        else false
    end as is_night

from seconds