from sqlalchemy.orm import Session

from app.database.models import Analysis

def create_analysis(db:Session,analysis:Analysis)->Analysis:
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def get_analysis(db:Session,analysis_id:str)->Analysis | None:
    return(
        db.query(Analysis)
        .filter(Analysis.analysis_id==analysis_id)
        .first()
    )

def list_analysis(db:Session)->list[Analysis]:
    return(
        db.query(Analysis)
        .order_by(Analysis.timestamp.desc())
        .all()
    )
