const COMMANDS = [
  { name: "clear", description: "Clear chat history" },
  { name: "commands", description: "Show available commands" },
]

function SlashMenu({ query, onSelect }) {
  const filtered = COMMANDS.filter((cmd) =>
    cmd.name.startsWith(query.slice(1))
  )

  if (filtered.length === 0) return null

  return (
    <div className="slash-menu">
      {filtered.map((cmd) => (
        <div
          key={cmd.name}
          className="slash-menu-item"
          onClick={() => onSelect(cmd.name)}
        >
          <span className="slash-cmd-name">/{cmd.name}</span>
          <span className="slash-cmd-desc">{cmd.description}</span>
        </div>
      ))}
    </div>
  )
}

export default SlashMenu