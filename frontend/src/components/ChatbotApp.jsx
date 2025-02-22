import { useState } from 'react';
import { Layout, Menu, Switch, Typography, Input, } from 'antd';
import {
  MessageOutlined,
  HistoryOutlined,
  SettingOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  SendOutlined,
  BulbOutlined,
  BulbFilled
} from '@ant-design/icons';
import '../index.css';

const { Header, Sider, Content, Footer } = Layout;
const { Title } = Typography;

const ChatbotApp = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const toggleCollapsed = () => {
    setCollapsed(!collapsed);
  };

  const toggleDarkMode = (checked) => {
    setDarkMode(checked);
  };

  return (
    <Layout style={{ minHeight: '100vh' }} className={darkMode ? 'dark-mode' : ''}>
      <Sider collapsible collapsed={collapsed} onCollapse={toggleCollapsed} theme={darkMode ? 'dark' : 'light'}>
        <div className="logo">
          <Title level={3} style={{ color: darkMode ? '#fff' : '#000' }}>Museum Chatbot</Title>
        </div>
        <Menu theme={darkMode ? 'dark' : 'light'} defaultSelectedKeys={['1']} mode="inline">
          <Menu.Item key="1" icon={<MessageOutlined />}>New Chat</Menu.Item>
          <Menu.Item key="2" icon={<HistoryOutlined />}>History</Menu.Item>
          <Menu.Item key="3" icon={<SettingOutlined />}>Settings</Menu.Item>
          <Menu.Item key="4">
            <span>Mode</span>
            <Switch
              checkedChildren={<BulbFilled />}
              unCheckedChildren={<BulbOutlined />}
              onChange={toggleDarkMode}
            />
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout>
        <Header style={{ background: darkMode ? '#001529' : '#fff', padding: '0 20px' }}>
          {collapsed ? <MenuUnfoldOutlined onClick={toggleCollapsed} /> : <MenuFoldOutlined onClick={toggleCollapsed} />}
        </Header>
        <Content style={{ margin: '20px', padding: '20px', background: darkMode ? '#141414' : '#fff' }}>
          <div style={{ minHeight: '70vh' }}>
            <Title level={4}>Type a message...</Title>
            <Input placeholder="Type a message..." suffix={<SendOutlined />} />
          </div>
        </Content>
        <Footer style={{ textAlign: 'center' }}>Museum Chatbot ©2025</Footer>
      </Layout>
    </Layout>
  );
};

export default ChatbotApp;
