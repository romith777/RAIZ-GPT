import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Plus, MessageSquare, Sun, Moon, User, Bot, Copy, Edit2, Check, ChevronLeft, ChevronRight, Square } from 'lucide-react';
import './index.css';
import LogoBlack from './assets/RAIZ_W.png';
import LogoWhite from './assets/RAIZ_B.png';

function App() {
  const [theme, setTheme] = useState('dark');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  
  // Tree Structure: { id: { id, role, content, parentId, childrenIds, timeTaken } }
  const [nodes, setNodes] = useState({});
  const [activeLeafId, setActiveLeafId] = useState(null);
  
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [reloadingNodeId, setReloadingNodeId] = useState(null);
  const [copiedId, setCopiedId] = useState(null);
  
  // Inline Editing
  const [editingNodeId, setEditingNodeId] = useState(null);
  const [editText, setEditText] = useState('');
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const abortControllerRef = useRef(null);

  const handleCancel = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
  };

  const getActivePath = () => {
    const path = [];
    let currentId = activeLeafId;
    while (currentId && nodes[currentId]) {
      path.unshift(nodes[currentId]);
      currentId = nodes[currentId].parentId;
    }
    return path;
  };

  const currentPath = getActivePath();
  const isEmpty = currentPath.length === 0;

  const toggleTheme = () => setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  const toggleSidebar = () => setIsSidebarOpen(prev => !prev);

  const scrollToBottom = () => {
    if (!isEmpty) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [activeLeafId, isLoading, nodes]);

  const getDeepestLeafId = (nodeId) => {
    let current = nodes[nodeId];
    while (current && current.childrenIds && current.childrenIds.length > 0) {
      current = nodes[current.childrenIds[current.childrenIds.length - 1]];
    }
    return current ? current.id : null;
  };

  const handleNav = (nodeId, direction) => {
    const node = nodes[nodeId];
    if (!node) return;
    
    let siblings = [];
    if (node.parentId && nodes[node.parentId]) {
      siblings = nodes[node.parentId].childrenIds;
    } else if (!node.parentId) {
      siblings = Object.values(nodes).filter(n => !n.parentId && n.role === 'user').map(n => n.id);
    }
    
    if (siblings.length <= 1) return;
    
    const currentIndex = siblings.indexOf(nodeId);
    let newIndex = currentIndex;
    
    if (direction === 'prev' && currentIndex > 0) newIndex = currentIndex - 1;
    if (direction === 'next' && currentIndex < siblings.length - 1) newIndex = currentIndex + 1;
    
    if (newIndex !== currentIndex) {
      const targetSiblingId = siblings[newIndex];
      setActiveLeafId(getDeepestLeafId(targetSiblingId));
    }
  };

  const handleSend = async (overrideText = null, overrideParentId = activeLeafId) => {
    const textToSend = overrideText !== null ? overrideText : input.trim();
    if (!textToSend) return;
    
    if (overrideText === null) {
      setInput('');
    }

    const userMsgId = Date.now().toString();
    const newUserNode = {
      id: userMsgId,
      role: 'user',
      content: textToSend,
      parentId: overrideParentId,
      childrenIds: []
    };

    setNodes(prev => {
      const nextNodes = { ...prev, [userMsgId]: newUserNode };
      if (overrideParentId && nextNodes[overrideParentId]) {
        nextNodes[overrideParentId] = {
          ...nextNodes[overrideParentId],
          childrenIds: [...nextNodes[overrideParentId].childrenIds, userMsgId]
        };
      }
      return nextNodes;
    });
    
    setActiveLeafId(userMsgId);
    setIsLoading(true);
    
    const startTime = Date.now();

    const formatTime = (ms) => {
      const totalSeconds = ms / 1000;
      if (totalSeconds < 60) return `${totalSeconds.toFixed(1)}s`;
      const minutes = Math.floor(totalSeconds / 60);
      const seconds = Math.floor(totalSeconds % 60);
      if (minutes < 60) return `${minutes}m ${seconds}s`;
      const hours = Math.floor(minutes / 60);
      const remainingMinutes = minutes % 60;
      return `${hours}h ${remainingMinutes}m`;
    };

    try {
      abortControllerRef.current = new AbortController();
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:7860';
      const response = await axios.post(`${apiUrl}/chat`, {
        instruction: textToSend
      }, {
        headers: { "ngrok-skip-browser-warning": "69420" } ,
        signal: abortControllerRef.current.signal
      });
      
      const endTime = Date.now();
      const timeTaken = formatTime(endTime - startTime);
      
      const aiMsgId = (Date.now() + 1).toString();
      const newAiNode = {
        id: aiMsgId,
        role: 'ai',
        content: response.data.response || 'No response generated.',
        parentId: userMsgId,
        childrenIds: [],
        timeTaken: timeTaken
      };
      
      setNodes(prev => {
        const nextNodes = { ...prev, [aiMsgId]: newAiNode };
        nextNodes[userMsgId] = {
          ...nextNodes[userMsgId],
          childrenIds: [...nextNodes[userMsgId].childrenIds, aiMsgId]
        };
        return nextNodes;
      });
      setActiveLeafId(aiMsgId);
    } catch (error) {
      console.error('Error fetching response:', error);
      const isCancelled = axios.isCancel(error);
      const endTime = Date.now();
      const timeTaken = formatTime(endTime - startTime);
      const aiMsgId = (Date.now() + 1).toString();
      const errorNode = {
        id: aiMsgId,
        role: 'ai',
        content: isCancelled ? 'Generation cancelled.' : `Error: ${error.response?.data?.error || 'Could not connect to the backend server.'}`,
        parentId: userMsgId,
        childrenIds: [],
        timeTaken: timeTaken
      };
      setNodes(prev => {
        const nextNodes = { ...prev, [aiMsgId]: errorNode };
        nextNodes[userMsgId] = {
          ...nextNodes[userMsgId],
          childrenIds: [...nextNodes[userMsgId].childrenIds, aiMsgId]
        };
        return nextNodes;
      });
      setActiveLeafId(aiMsgId);
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!isLoading && input.trim()) {
        handleSend();
      }
    }
  };

  const handleNewChat = () => {
    if (isLoading) {
      handleCancel();
    }
    setNodes({});
    setActiveLeafId(null);
    setInput('');
    setIsSidebarOpen(false);
    inputRef.current?.focus();
  };

  const handleCopy = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleEditStart = (msg) => {
    setEditingNodeId(msg.id);
    setEditText(msg.content);
  };

  const handleEditSubmit = async (msg) => {
    setEditingNodeId(null);
    if (editText.trim() === msg.content) return; // No change
    
    if (isLoading) {
      handleCancel();
    }

    // Create a new user node for the branch
    const userMsgId = Date.now().toString();
    const newUserNode = {
      id: userMsgId,
      role: 'user',
      content: editText.trim(),
      parentId: msg.parentId,
      childrenIds: []
    };

    setNodes(prev => {
      const nextNodes = { ...prev, [userMsgId]: newUserNode };
      // Link this new user node to the original parent, creating the branch < 2 / 2 >
      if (msg.parentId && nextNodes[msg.parentId]) {
        nextNodes[msg.parentId] = {
          ...nextNodes[msg.parentId],
          childrenIds: [...nextNodes[msg.parentId].childrenIds, userMsgId]
        };
      }
      return nextNodes;
    });

    const path = getActivePath();
    const userNodeIndex = path.findIndex(n => n.id === msg.id);
    const nodesToCopy = [];
    if (userNodeIndex !== -1 && userNodeIndex + 1 < path.length) {
      for (let i = userNodeIndex + 2; i < path.length; i++) {
        nodesToCopy.push(path[i]);
      }
    }

    setActiveLeafId(userMsgId);
    setIsLoading(true);
    
    const startTime = Date.now();
    const formatTime = (ms) => {
      const totalSeconds = ms / 1000;
      if (totalSeconds < 60) return `${totalSeconds.toFixed(1)}s`;
      const minutes = Math.floor(totalSeconds / 60);
      const seconds = Math.floor(totalSeconds % 60);
      if (minutes < 60) return `${minutes}m ${seconds}s`;
      const hours = Math.floor(minutes / 60);
      const remainingMinutes = minutes % 60;
      return `${hours}h ${remainingMinutes}m`;
    };

    try {
      abortControllerRef.current = new AbortController();
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:7860';
      const response = await axios.post(`${apiUrl}/chat`, {
        instruction: editText.trim()
      }, {
        headers: { "ngrok-skip-browser-warning": "69420" },
        signal: abortControllerRef.current.signal
      });
      
      const endTime = Date.now();
      const timeTaken = formatTime(endTime - startTime);
      
      const aiMsgId = (Date.now() + 1).toString();
      const newAiNode = {
        id: aiMsgId,
        role: 'ai',
        content: response.data.response || 'No response generated.',
        parentId: userMsgId,
        childrenIds: [],
        timeTaken: timeTaken
      };
      
      let lastCopiedId = aiMsgId;

      setNodes(prev => {
        const nextNodes = { ...prev, [aiMsgId]: newAiNode };
        nextNodes[userMsgId] = {
          ...nextNodes[userMsgId],
          childrenIds: [aiMsgId]
        };
        
        let parentForCopied = aiMsgId;
        
        for (const oldNode of nodesToCopy) {
          const newNodeId = Date.now().toString() + Math.random().toString().slice(2, 6);
          const copiedNode = {
            ...oldNode,
            id: newNodeId,
            parentId: parentForCopied,
            childrenIds: []
          };
          nextNodes[newNodeId] = copiedNode;
          nextNodes[parentForCopied] = {
            ...nextNodes[parentForCopied],
            childrenIds: [newNodeId]
          };
          parentForCopied = newNodeId;
          lastCopiedId = newNodeId;
        }
        
        return nextNodes;
      });

      setActiveLeafId(prevId => prevId === userMsgId ? lastCopiedId : prevId);

    } catch (error) {
      console.error('Error fetching response:', error);
      const isCancelled = axios.isCancel(error);
      const endTime = Date.now();
      const timeTaken = formatTime(endTime - startTime);
      const aiMsgId = (Date.now() + 1).toString();
      const errorNode = {
        id: aiMsgId,
        role: 'ai',
        content: isCancelled ? 'Generation cancelled.' : `Error: ${error.response?.data?.error || 'Could not connect to the backend server.'}`,
        parentId: userMsgId,
        childrenIds: [],
        timeTaken: timeTaken
      };
      
      let lastCopiedId = aiMsgId;

      setNodes(prev => {
        const nextNodes = { ...prev, [aiMsgId]: errorNode };
        nextNodes[userMsgId] = {
          ...nextNodes[userMsgId],
          childrenIds: [aiMsgId]
        };
        
        let parentForCopied = aiMsgId;
        
        for (const oldNode of nodesToCopy) {
          const newNodeId = Date.now().toString() + Math.random().toString().slice(2, 6);
          const copiedNode = {
            ...oldNode,
            id: newNodeId,
            parentId: parentForCopied,
            childrenIds: []
          };
          nextNodes[newNodeId] = copiedNode;
          nextNodes[parentForCopied] = {
            ...nextNodes[parentForCopied],
            childrenIds: [newNodeId]
          };
          parentForCopied = newNodeId;
          lastCopiedId = newNodeId;
        }
        
        return nextNodes;
      });

      setActiveLeafId(prevId => prevId === userMsgId ? lastCopiedId : prevId);

    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  return (
    <div className="app-layout" data-theme={theme}>
      
      {/* Mobile Sidebar Overlay */}
      <div 
        className={`sidebar-overlay ${isSidebarOpen ? 'open' : ''}`} 
        onClick={() => setIsSidebarOpen(false)}
      ></div>

      {/* Floating Toggle Button (Visible when sidebar is closed) */}
      {!isSidebarOpen && (
        <button className="floating-toggle-btn" onClick={toggleSidebar} title="Open Sidebar">
          <ChevronRight size={24} />
        </button>
      )}

      {/* Sidebar for Chat History */}
      <div className={`sidebar ${!isSidebarOpen ? 'closed' : ''}`}>
        
        <div className="sidebar-header">
          <img src={theme === 'light' ? LogoBlack : LogoWhite} alt="RAIZ" className="sidebar-logo" />
          <button className="sidebar-toggle-btn" onClick={toggleSidebar} title="Close Sidebar">
            <ChevronLeft size={24} />
          </button>
        </div>

        <button className="new-chat-btn" onClick={handleNewChat}>
          <Plus size={18} />
          New chat
        </button>
        
        <div className="history-list">
          <div className={`history-item ${!isEmpty ? 'active' : ''}`}>
            <MessageSquare size={16} />
            <span>Current Conversation</span>
          </div>
        </div>

        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="avatar user">
              <User size={16} />
            </div>
            <span>Sign in</span>
          </div>
        </div>
      </div>

      {/* Main Chat Interface */}
      <div className={`main-chat ${isEmpty ? 'is-empty' : ''}`}>
        <div className="header">
          <div className="header-right">
            <button className="theme-toggle" onClick={toggleTheme} title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} mode`}>
              {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
            </button>
          </div>
        </div>

        {/* Hero Section shown when empty */}
        <div className="hero-section">
          <h1>How can I help you today?</h1>
        </div>

        <div className="chat-messages">
          {currentPath.map((msg) => {
            const isEditing = editingNodeId === msg.id;
            
            let displaySiblings = [];
            let navNodeId = msg.id;

            if (msg.role === 'user') {
              if (msg.parentId && nodes[msg.parentId]) {
                displaySiblings = nodes[msg.parentId].childrenIds;
              } else if (!msg.parentId) {
                displaySiblings = Object.values(nodes).filter(n => !n.parentId && n.role === 'user').map(n => n.id);
              }
            } else if (msg.role === 'ai') {
              const parentNode = nodes[msg.parentId];
              if (parentNode) {
                if (parentNode.parentId && nodes[parentNode.parentId]) {
                  displaySiblings = nodes[parentNode.parentId].childrenIds;
                } else if (!parentNode.parentId) {
                  displaySiblings = Object.values(nodes).filter(n => !n.parentId && n.role === 'user').map(n => n.id);
                }
                navNodeId = parentNode.id;
              }
            }
            
            let siblingCount = displaySiblings.length || 1;
            let currentIndex = displaySiblings.indexOf(navNodeId);
            if (currentIndex === -1) currentIndex = 0;

            return (
              <div key={msg.id} className={`message-wrapper ${msg.role}`}>
                <div className="message-content">
                  
                  {msg.role === 'user' && !isEditing && (
                    <div className="message-header">
                      <div className="avatar user">
                        <User size={16} />
                      </div>
                      <span>You</span>
                    </div>
                  )}

                  {msg.role === 'ai' && !isEditing && (
                    <div className="message-header ai-header">
                      <span>Response</span>
                      {msg.timeTaken && reloadingNodeId !== msg.id && <span className="time-taken">{msg.timeTaken}</span>}
                    </div>
                  )}

                  {isEditing ? (
                    <div className="edit-container">
                      <textarea
                        className="edit-textarea"
                        value={editText}
                        onChange={(e) => setEditText(e.target.value)}
                        autoFocus
                      />
                      <div className="edit-actions">
                        <button className="btn-cancel" onClick={() => setEditingNodeId(null)}>Cancel</button>
                        <button className="btn-save" onClick={() => handleEditSubmit(msg)}>Save</button>
                      </div>
                    </div>
                  ) : reloadingNodeId === msg.id ? (
                    <div className="loading-dots">
                      <span className="dot"></span>
                      <span className="dot"></span>
                      <span className="dot"></span>
                      <span className="dot"></span>
                    </div>
                  ) : (
                    <div className="message-bubble">
                      {msg.content}
                    </div>
                  )}

                  <div className="message-actions">
                    {siblingCount > 1 && msg.role === 'user' && (
                      <div className="branch-nav">
                        <button disabled={currentIndex === 0} onClick={() => handleNav(navNodeId, 'prev')} title="Previous Version">
                          <ChevronLeft size={16} />
                        </button>
                        <span>{currentIndex + 1} / {siblingCount}</span>
                        <button disabled={currentIndex === siblingCount - 1} onClick={() => handleNav(navNodeId, 'next')} title="Next Version">
                          <ChevronRight size={16} />
                        </button>
                      </div>
                    )}

                    {msg.role === 'ai' && reloadingNodeId !== msg.id && (
                      <button 
                        className="action-btn" 
                        onClick={() => handleCopy(msg.content, msg.id)}
                        title="Copy response"
                      >
                        {copiedId === msg.id ? <Check size={16} /> : <Copy size={16} />}
                      </button>
                    )}
                    
                    {!isEditing && msg.role === 'user' && (
                      <button 
                        className="action-btn" 
                        onClick={() => handleEditStart(msg)}
                        title="Edit prompt"
                      >
                        <Edit2 size={16} />
                      </button>
                    )}
                  </div>

                </div>
              </div>
            );
          })}
          
          {isLoading && !reloadingNodeId && (
            <div className="message-wrapper ai">
              <div className="message-content">
                <div className="loading-dots">
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area-wrapper">
          <div className="input-container">
            <textarea
              ref={inputRef}
              className="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Message your assistant..."
              rows={1}
            />
            {isLoading ? (
              <button 
                className="send-btn stop-btn" 
                onClick={handleCancel}
                title="Stop generating"
              >
                <div className="stop-icon-wrapper">
                  <div className="spinner-ring"></div>
                  <Square fill="currentColor" size={12} className="inner-square" />
                </div>
              </button>
            ) : (
              <button 
                className="send-btn" 
                onClick={() => handleSend(null, activeLeafId)} 
                disabled={!input.trim()}
              >
                <Send size={18} />
              </button>
            )}
          </div>
          <div className="disclaimer-text">
            RAIZ is an AI, and it can make mistakes.
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

