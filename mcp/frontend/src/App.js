import { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const sendQuery = async () => {
    if (!query.trim()) return;

    const newMessages = [...messages, { role: "user", content: query }];
    setMessages(newMessages);
    setQuery("");
    setLoading(true);

    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();

      const reply =
        data.type === "tool"
          ? `🔧 Tool: ${data.tool_name}\n\n${data.output.join("\n")}`
          : data.output;

      setMessages([...newMessages, { role: "assistant", content: reply }]);
    } catch (err) {
      setMessages([
        ...newMessages,
        { role: "assistant", content: "❌ Error contacting server" },
      ]);
    }

    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.header}>MCP AI Assistant</h2>

      <div style={styles.chatBox}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              ...styles.message,
              ...(msg.role === "user"
                ? styles.userMessage
                : styles.botMessage),
            }}
          >
            {msg.content}
          </div>
        ))}
        {loading && <div style={styles.loading}>Thinking...</div>}
      </div>

      <div style={styles.inputArea}>
        <input
          style={styles.input}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask something..."
        />
        <button style={styles.button} onClick={sendQuery}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    fontFamily: "Inter, sans-serif",
    background: "#0f172a",
    color: "#fff",
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    padding: "20px",
  },
  header: {
    textAlign: "center",
  },
  chatBox: {
    flex: 1,
    overflowY: "auto",
    background: "#1e293b",
    padding: "10px",
    borderRadius: "10px",
  },
  message: {
    padding: "10px",
    margin: "10px 0",
    borderRadius: "10px",
    maxWidth: "70%",
    whiteSpace: "pre-wrap",
  },
  userMessage: {
    background: "#2563eb",
    alignSelf: "flex-end",
  },
  botMessage: {
    background: "#334155",
    alignSelf: "flex-start",
  },
  inputArea: {
    display: "flex",
    marginTop: "10px",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "8px",
    border: "none",
    marginRight: "10px",
  },
  button: {
    padding: "10px 20px",
    background: "#22c55e",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },
  loading: {
    fontStyle: "italic",
    opacity: 0.7,
  },
};

export default App;