from tailor.core.matrix.grid_neo_theone_base import Base 

class AndrewArchitectOrm(Base):
    """
    [기획 홀딩 구역]
    - 실제 DB 테이블을 생성하지 않고 설계만 유지합니다.
    """
    # 🛡️ 이 한 줄이 들어가면 pass와 동일하게 작동하면서 에러가 완벽히 소멸합니다.
    __abstract__ = True