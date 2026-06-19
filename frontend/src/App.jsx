import { useState } from "react"
import "./App.css"
import SlashMenu from "./components/SlashMenu"

const HELP_MESSAGE = `Available commands:
/clear — Clear chat history
/commands — Show available commands`

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  const showSlashMenu = input.startsWith("/") && !input.includes(" ")

  function handleSelect(commandName) {
    if (commandName === "clear") {
      setMessages([])
    } else if (commandName === "commands") {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: HELP_MESSAGE },
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
      const agentMessage = { role: "assistant", content: data.response }
      setMessages([...updatedMessages, agentMessage])
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") sendMessage()
  }

  return (
    <div className="container">
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
            <p className="loading">Thinking...</p>
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
          <button onClick={sendMessage} disabled={loading}>Send</button>
        </div>
      </div>
    </div>
  )
}

export default App