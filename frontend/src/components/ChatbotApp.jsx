import { useState, useEffect, useRef } from 'react';
import { Layout, Menu, Switch, Typography, Input, Button } from 'antd';
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
import MessageBubble from './MessageBubble';
import '../index.css';

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

const ChatbotApp = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [messages, setMessages] = useState([
    { text: 'Hello! How can I help you today?', isSent: false },
    { text: 'I would like to know more about the museum.', isSent: true },
    { text: 'Sure! The museum has a rich history and many exhibits.', isSent: false }
  ]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const toggleCollapsed = () => {
    setCollapsed(!collapsed);
  };

  const toggleDarkMode = (checked) => {
    setDarkMode(checked);
  };

  const handleSendMessage = () => {
    if (inputValue.trim()) {
      const newMessages = [...messages, { text: inputValue, isSent: true }];
      setMessages(newMessages);
      setInputValue('');

      // Hardcoded response
      setTimeout(() => {
        const response = getResponse(inputValue);
        setMessages([...newMessages, { text: response, isSent: false }]);
      }, 500);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const getResponse = (message) => {
    // Placeholder for actual server response logic
    if (message.toLowerCase() === 'hi') {
      return 'How can I help you?';
    }
    return 'This is a placeholder response from the server.';
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <Layout style={{ minHeight: '100vh' }} className={darkMode ? 'dark-mode' : ''}>
      <Sider collapsible collapsed={collapsed} onCollapse={toggleCollapsed} theme={darkMode ? 'dark' : 'light'} style={{ height: '100vh', position: 'fixed', left: 0 }}>
        {!collapsed && (
          <div className="logo mt-2 p-1">
            <Title level={3} style={{color: darkMode ? '#fff' : '#000', transition: 'color 0.3s ease' }}>Museum Chatbot</Title>
          </div>
        )}
        <Menu theme={darkMode ? 'dark' : 'light'} defaultSelectedKeys={['1']} mode="inline">
          <Menu.Item key="1" icon={<MessageOutlined />}>New Chat</Menu.Item>
          <Menu.Item key="2" icon={<HistoryOutlined />}>History</Menu.Item>
          <Menu.Item key="3" icon={<SettingOutlined />}>Settings</Menu.Item>
        </Menu>
      </Sider>
      <Layout style={{ marginLeft: collapsed ? 80 : 200 }}>
        <Header style={{ background: darkMode ? '#001529' : '#fff', padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', transition: 'background 0.3s ease' }}>
          {collapsed ? <MenuUnfoldOutlined onClick={toggleCollapsed} /> : <MenuFoldOutlined onClick={toggleCollapsed} />}
          <Switch
            checkedChildren={<BulbFilled />}
            unCheckedChildren={<BulbOutlined />}
            onChange={toggleDarkMode}
          />
        </Header>
        <Content style={{ background: darkMode ? '#141414' : '#fff', position: 'relative', overflow: 'hidden', height: 'calc(100vh - 64px)', transition: 'background 0.3s ease' }}>
          <div className="content-container" style={{ paddingBottom: '60px', overflowY: 'auto', height: '100%' }}>
            {messages.map((msg, index) => (
              <MessageBubble key={index} message={msg.text} isSent={msg.isSent} />
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className={`input-container ${darkMode ? 'dark-mode' : 'light-mode'}`} style={{ width: collapsed ? 'calc(100% - 80px)' : 'calc(100% - 300px)', position: 'fixed', bottom: '10px', left: collapsed ? '80px' : '200px', transition: 'width 0.3s ease' }}>
            <Input
              placeholder="Type a message..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              style={{ flex: 1, marginRight: '10px' }}
            />
            <Button type="primary" icon={<SendOutlined />} onClick={handleSendMessage} style={{ background: darkMode ? '#333' : '#1890ff', color: darkMode ? '#fff' : '#fff', transition: 'background 0.3s ease, color 0.3s ease' }} />
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default ChatbotApp;
