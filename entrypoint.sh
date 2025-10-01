#!/bin/bash

/bin/ollama serve &

pid=$!
sleep 5

echo "Pull model llama3.1..."
ollama pull llama3.1
echo "Model pulled."

wait $pid
