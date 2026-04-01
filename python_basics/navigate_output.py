ai_output = {
  "id": "resp_68af4030592c81938ec0a5fbab4a3e9f05438e46b5f69a3b",
  "object": "response",
  "created_at": 1756315696,
  "model": "gpt-5-2025-08-07",
  "output": [
    {
      "id": "rs_68af4030baa48193b0b43b4c2a176a1a05438e46b5f69a3b",
      "type": "reasoning",
      "content": [],
      "summary": []
    },
    {
      "id": "msg_68af40337e58819392e935fb404414d005438e46b5f69a3b",
      "type": "message",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "annotations": [],
          "logprobs": [],
          "text": "Under a quilt of moonlight, a drowsy unicorn wandered through quiet meadows, brushing blossoms with her glowing horn so they sighed soft lullabies that carried every dreamer gently to sleep."
        }
      ],
      "role": "assistant"
    }
  ],
}

print(ai_output['output'][1]['content'][0]['text'])