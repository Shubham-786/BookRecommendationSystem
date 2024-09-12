from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "t5-small"
# We can use 't5-base' or 't5-large' for better performance
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def generate_summary(text: str) -> str:
    """
    Generating a summary of the given text using a pre-trained T5 model.

    Args:
        text (str): The text to be summarized.

    Returns:
        str: The generated summary.
    """
    input_text = "summarize: " + text
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    
    summary_ids = model.generate(
        inputs,
        max_length=150,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
