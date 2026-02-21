# optimized_business_ai.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import logging
import time
from typing import Dict, List, Optional
import os

class OptimizedBusinessConsultingAI:
    def __init__(self, access_token=None):
        """
        Initialize the Business Consulting AI with optimized settings for MSME use cases
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.access_token = access_token
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        try:
            self.logger.info(f"Initializing AI model on {self.device}")
            
            # Load tokenizer and model with optimized settings
            model_name = "Qwen/Qwen3-0.6B"
            
            # Set up proper loading parameters for web deployment
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                token=access_token,
                trust_remote_code=True
            )
            
            # Load model with memory optimization
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                token=access_token,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                low_cpu_mem_usage=True
            )
            
            # Add padding token if not exists
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            self.logger.info("✅ AI model loaded successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize AI model: {str(e)}")
            raise
    
    def generate_response(self, question: str, category: str = "general", max_length: int = 512) -> str:
        """
        Generate a business consulting response based on the question and category
        
        Args:
            question (str): The business question to answer
            category (str): Business category for context (e.g., finance, marketing, operations)
            max_length (int): Maximum length of generated response
            
        Returns:
            str: Generated business consulting response
        """
        try:
            # Add context based on category
            context_prompts = {
                "general": "You are a business consultant specializing in helping MSMEs. Provide practical, actionable advice.",
                "finance": "You are a financial advisor for small businesses. Focus on cash flow management, budgeting, and financial planning.",
                "marketing": "You are a marketing consultant for small businesses. Provide strategies for digital marketing, branding, and customer acquisition.",
                "operations": "You are an operations consultant for MSMEs. Focus on process improvement, efficiency, and resource optimization.",
                "hr": "You are an HR consultant for small businesses. Provide guidance on employee management, recruitment, and workplace culture."
            }
            
            # Build prompt with context
            context = context_prompts.get(category.lower(), context_prompts["general"])
            prompt = f"{context} Question: {question}\n\nAnswer:"
            
            self.logger.info(f"Processing question in category '{category}': {question[:50]}...")
            
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=1024,
                padding=True
            ).to(self.device)
            
            # Generate response with optimized parameters
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            generated_text = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:], 
                skip_special_tokens=True
            ).strip()
            
            self.logger.info("Response generated successfully")
            return generated_text
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            self.logger.error(error_msg)
            return f"Sorry, I encountered an error processing your request: {str(e)}"
    
    def batch_generate(self, questions: List[str], category: str = "general") -> List[str]:
        """
        Generate responses for multiple questions
        
        Args:
            questions (List[str]): List of business questions
            category (str): Business category for context
            
        Returns:
            List[str]: List of generated responses
        """
        responses = []
        for question in questions:
            response = self.generate_response(question, category)
            responses.append(response)
        return responses
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model
        
        Returns:
            Dict: Model information including device, parameters, etc.
        """
        try:
            if hasattr(self.model, 'config'):
                config = self.model.config
                return {
                    "model_name": config._name_or_path,
                    "device": str(self.device),
                    "torch_dtype": str(self.model.dtype),
                    "parameters": f"{self.model.num_parameters() / 1e6:.2f}M"
                }
            else:
                return {
                    "model_name": "Qwen3-0.6B",
                    "device": str(self.device),
                    "torch_dtype": str(self.model.dtype) if hasattr(self.model, 'dtype') else "unknown"
                }
        except Exception as e:
            return {"error": f"Could not retrieve model info: {str(e)}"}
    
    def cleanup(self):
        """
        Clean up resources when shutting down
        """
        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            self.logger.info("Resources cleaned up successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")

# Example usage for testing
if __name__ == "__main__":
    # This is for testing purposes only - not used in web app
    try:
        # Initialize without access token for local testing (you'll need to add your token)
        consultant = OptimizedBusinessConsultingAI()
        
        # Test a simple question
        test_question = "How can I improve cash flow management for my small business?"
        response = consultant.generate_response(test_question, "finance")
        print("Test Response:")
        print(response)
        
    except Exception as e:
        print(f"Error in test: {e}")
