from abc import ABCMeta, abstractmethod # 객체지향 인터페이스로 선언하기 위해 ABCMeta 클래스를 이용
from user.domain.user import User

class IUserRepository(metaclass=ABCMeta):
    # 인터페이스임을 명시적으로 나타내기 위해 클래스 이름 앞에 I를 붙임
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError
    
    @abstractmethod
    def find_by_email(sefl, email: str) -> User:
        """
        이메일로 유저를 검색한다.
        검색한 유저가 없을 경우 422 에러를 발생시킨다.
        """
        raise NotImplementedError