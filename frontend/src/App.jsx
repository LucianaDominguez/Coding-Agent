import { useState } from "react"
import "./App.css"
import SlashMenu from "./components/SlashMenu"

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  const isHome = messages.length === 0
  const showSlashMenu = input.startsWith("/") && !input.includes(" ")

  function handleSelect(commandName) {
    if (commandName === "clear") {
      setMessages([])
    } else if (commandName === "commands") {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Available commands:\n/clear — Clear chat history\n/commands — Show available commands" },
      ])
    }
    setInput("")
  }

  async function sendMessage() {
    if (!input.trim()) return
    if (input.startsWith("/")) return

    const userMessage = { role: "user", content: input }
    const updatedMessages = [...messages, userMessage]

    setMessages(updatedMessages)
    setInput("")
    setLoading(true)

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: updatedMessages }),
      })
      const data = await response.json()
      setMessages([...updatedMessages, { role: "assistant", content: data.response }])
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (isHome) {
    return (
      <div className="app">
        <div className="home-view">
          <h1 className="home-title">Coding Agent</h1>
          <div className="home-input-wrapper">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything..."
              rows={2}
            />
            <div className="home-input-footer">
              <button className="send-btn" onClick={sendMessage}>↑</button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <div className="chat-view">
        <div className="chat-window">
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <span className="label">{msg.role === "user" ? "You" : "Agent"}</span>
              <p>{msg.content}</p>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <span className="label">Agent</span>
              <p className="thinking">
                <span>.</span><span>.</span><span>.</span>
              </p>
            </div>
          )}
        </div>

        <div className="input-area">
          {showSlashMenu && (
            <SlashMenu query={input} onSelect={handleSelect} />
          )}
          <div className="input-bar">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Message... (type / for commands)"
              disabled={loading}
            />
            <button onClick={sendMessage} disabled={loading}>↑</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App