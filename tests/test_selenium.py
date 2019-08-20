from selenium import webdriver
import unittest
import re
import time
import threading
from app import create_app, db
from app.models import User, Role, Post


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
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='john@example.com',
                         username='john', password='cat',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # 在一个线程中启动flask服务器
            threading.Thread(target=cls.app.run).start()

            time.sleep(1)

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

    def test_admin_home_page(self):
        # 进入首页
        self.client.get('http://localhost:5000/')
        # print(self.client.page_source)
        self.assertTrue(re.search('Hello,\s+Stranger', self.client.page_source))
        #  <p>Pleased to meet you!</p>

        # 进入登录页面
        self.client.find_element_by_link_text('Log In').click()
        # print(self.client.page_source)
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)
        # 登录
        self.client.find_element_by_name('email').\
            send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        print(self.client.page_source)
        self.assertTrue(re.search('Hello,\s+john', self.client.page_source))

        # 进入用户个人资料页面
        self.client.find_element_by_link_text('john').click()
        # print(self.client.page_source)
        self.assertTrue('<h1>User</h1>' in self.client.page_source)


