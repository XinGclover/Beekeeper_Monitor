from __future__ import annotations

def create_scraping_job(conn, source_id: int) -> int:
    sql = """
        INSERT INTO ingestion.scraping_job (source_id, status)
        VALUES (%s, 'running')
        RETURNING job_id
    """

    with conn.cursor() as cur:
        cur.execute(sql, (source_id,))
        job_id = cur.fetchone()[0]

    return job_id

def update_scraping_job_status(conn, job_id: int, status: str):
    sql = """
        UPDATE ingestion.scraping_job
        SET status = %s
        WHERE job_id = %s
    """

    with conn.cursor() as cur:
        cur.execute(sql, (status, job_id))

def fail_scraping_job(conn, job_id: int, error_message: str) -> None:
    sql = """
        UPDATE ingestion.scraping_job
        SET status = 'failed',
            error_message = %s
        WHERE job_id = %s
    """
    with conn.cursor() as cur:
        cur.execute(sql, (error_message, job_id))