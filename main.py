from utils import ask_ollama

print("Testing Ollama connection...")

answer = ask_ollama("Say hello in one sentence.")

print("\nOllama Response:")
print(answer)