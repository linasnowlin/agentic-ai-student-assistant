import os

from dotenv import load_dotenv
from groq import Groq, GroqError

from agent import run_agent


# Load environment variables
load_dotenv()


# Get configuration
api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


# Check API key
if not api_key:
    print("❌ GROQ_API_KEY not found.")
    print("Add it to your .env file:")
    print("GROQ_API_KEY=your_api_key_here")
    exit(1)


# Create Groq client
client = Groq(api_key=api_key)


# Conversation history
messages = []


def show_tool(name: str, arguments: dict, result: str) -> None:
    """Display the tool used by the agent."""

    print("\n🔧 Tool Used:", name)
    print("Arguments:", arguments)
    print("Result:", result)
    print()


def main():

    print("=" * 60)
    print("🤖 Agentic AI - Student Assistant")
    print("=" * 60)

    print("Model:", model)

    print("\nAvailable tools:")
    print("  🧮 Calculator")
    print("  🎓 Student Information")
    print("  📊 Attendance")

    print("\nThe agent automatically decides which tool to use.")
    print("Type 'exit' or 'quit' to stop.")
    print("Type 'clear' to clear the conversation.")

    print("=" * 60)


    while True:

        try:

            # Get user input
            prompt = input("\n👤 You: ").strip()


            # Ignore empty input
            if not prompt:
                continue


            # Exit
            if prompt.lower() in ["exit", "quit"]:

                print("\n👋 Goodbye!")
                break


            # Clear conversation
            if prompt.lower() == "clear":

                messages.clear()

                print("🧹 Conversation cleared.")
                continue


            # Add user message
            messages.append({
                "role": "user",
                "content": prompt
            })


            print("\n🤖 Agent: Thinking...")


            # Run the agent
            answer = run_agent(
                client,
                model,
                messages,
                on_tool=show_tool,
            )


            # Display final answer
            print("\n🤖 Agent:", answer)


            # Add assistant response to conversation
            messages.append({
                "role": "assistant",
                "content": answer
            })


        except GroqError as error:

            print("\n❌ Groq request failed:")
            print(error)


        except KeyboardInterrupt:

            print("\n\n👋 Goodbye!")
            break


        except Exception as error:

            print("\n❌ Error:")
            print(error)


# Start the program
if __name__ == "__main__":
    main()