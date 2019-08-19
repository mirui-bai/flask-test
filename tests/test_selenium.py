from selenium import webdriver
import unittest
import threading
from app import create_app, db
from app.models import User, Role, Post, Comment


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # 启动goggle chrome
        try:
            cls.client = webdriver.Chrome()
        except:
            pass
        # 如果无法启动游览器，则跳过测试
        if cls.client:
            # 创建程序
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # 禁止日志，保持输出简洁
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            # 创建数据库,使用虚拟数据填充数据库
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            # 添加管理员
            admin_role = Role.query.filter_by(permission=0xff).first()
            admin = User(email='john@example.com',
                         username='john',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # 在一个线程中启动flask服务器
            threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # 关闭Flask服务器和游览器
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            # 销毁数据
            db.drop_all()
            db.session.remove()

            # 删除程序上下文
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('web browser not available')

    def tearDown(self):
        pass



