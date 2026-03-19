--Den visar vilka sensorer som finns på varje hive som reglerna pekar på.

--Men ännu bättre är denna, som visar om metric också matchar:
select
    art.rule_id,
    ar.name as rule_name,
    ar.metric_type_id,
    art.target_id as hive_id,
    s.sensor_id,
    s.sensor_type_id,
    case
        when ar.metric_type_id = 1 and s.sensor_type_id = 1 then 'OK'
        when ar.metric_type_id = 2 and s.sensor_type_id = 2 then 'OK'
        when ar.metric_type_id = 6 and s.sensor_type_id = 3 then 'OK'
        else 'WRONG'
    end as match_status
from ingestion.alarm_rule_target art
join ingestion.alarm_rule ar
  on ar.rule_id = art.rule_id
left join ingestion.sensor s
  on s.hive_id = art.target_id
where art.target_type_id = 3
order by art.rule_id, s.sensor_id;


select
    ar.rule_id,
    ar.name as rule_name,
    ar.metric_type_id,
    art.target_id as hive_id,
    s.sensor_id,
    s.sensor_type_id
from ingestion.alarm_rule_target art
join ingestion.alarm_rule ar
  on ar.rule_id = art.rule_id
join ingestion.sensor s
  on s.hive_id = art.target_id
where art.target_type_id = 3
  and (
      (ar.metric_type_id = 1 and s.sensor_type_id = 1) or
      (ar.metric_type_id = 2 and s.sensor_type_id = 2) or
      (ar.metric_type_id = 6 and s.sensor_type_id = 3)
  )
order by ar.rule_id, s.sensor_id;



select count(*) 
from ingestion.alarm_rule_target;


select *
from ingestion.alarm_rule_target
order by rule_id;

select rule_id, name, metric_type_id
from ingestion.alarm_rule
order by rule_id;

TRUNCATE TABLE ingestion.alarm_rule RESTART IDENTITY CASCADE;