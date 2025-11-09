from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from crewai import Agent, Task, Crew
from litellm import completion

app = FastAPI(title="Bangladesh AI Tax Helper")

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaxSummaryRequest(BaseModel):
    user_name: str
    age: int
    profession: str
    bank_statement: str

# Localized LLM Wrapper
class GeminiLLM:
    def __init__(self, model_name="gemini/gemini-2.0-flash-lite", temperature=0.2):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = "[Your Gemini API Key]"

    def run(self, messages):
        response = completion(
            model=self.model_name,
            messages=messages,
            api_key=self.api_key,
            litellm_provider="google",
            temperature=self.temperature
        )
        return response["choices"][0]["message"]["content"]

    def __call__(self, prompt):
        return self.run([{"role": "user", "content": prompt}])


llm = GeminiLLM()

@app.post("/generate-tax-summary")
async def generate_tax_summary(request: TaxSummaryRequest):
    user_name = request.user_name
    age = request.age
    profession = request.profession
    bank_statement = request.bank_statement

    # --- AGENTS (Bangladesh context) ---
    doc_parsing_agent = Agent(
        role='Bank Statement Analyzer',
        goal='Extract structured income and expense data from Bangladeshi bank statements',
        backstory='Expert in parsing Bangladeshi bank data formats and identifying deposits/withdrawals.',
        llm=llm
    )

    income_classifier = Agent(
        role='Income Classifier (Bangladesh)',
        goal='Classify income into Salary, Business, Agriculture, Freelance, or Other categories based on Bangladesh NBR heads.',
        backstory='Specialist in local tax categorization according to NBR Bangladesh.',
        llm=llm
    )

    deduction_agent = Agent(
        role='Tax Deduction Advisor (BD)',
        goal='Identify deductions under Bangladesh Income Tax Ordinance (e.g., Zakat, Provident Fund, Investment Allowance).',
        backstory='Knows the latest rules from NBR and eligible rebates for individuals.',
        llm=llm
    )

    tax_calc_agent = Agent(
        role='Bangladesh Tax Calculator',
        goal='Compute tax as per NBR slabs (0% up to 3.5 lakh, 10% up to 7 lakh, etc.) with rebates.',
        backstory='Accurately calculates tax payable under the 2024–25 Bangladesh personal income tax structure.',
        llm=llm
    )

    optimization_agent = Agent(
        role='Tax Optimization Consultant (BD)',
        goal='Recommend best ways to reduce taxable income and provide a clear Bangla summary report.',
        backstory='Creates simple summaries for Bangladeshi users with suggestions for next year’s savings.',
        llm=llm
    )

    # --- TASKS ---
    parse_task = Task(
        description=f"""
        Parse the bank statement of {user_name}, age {age}, profession {profession}.
        Extract all salary, income, business transactions, and investments.
        Statement (BD format):
        {bank_statement}
        """,
        expected_output="JSON with categorized transactions in BDT",
        agent=doc_parsing_agent
    )

    classify_task = Task(
        description="Classify all incomes as per Bangladesh NBR heads (Salary, Business, Agriculture, Freelance, Other).",
        expected_output="Structured income classification",
        agent=income_classifier
    )

    deduction_task = Task(
        description="Identify all deductions and rebates applicable in Bangladesh (Zakat, PF, Investments, Donations).",
        expected_output="List of eligible deductions and rebate calculations",
        agent=deduction_agent
    )

    tax_task = Task(
        description="Compute total tax as per Bangladesh NBR slab 2024–25 (3.5L exempt, 10%, 15%, 20%, 25%).",
        expected_output="Tax computation table in BDT",
        agent=tax_calc_agent
    )

    optimize_task = Task(
        description=f"""
        Generate a final report for {user_name} in Bangla summarizing tax details,
        deductions, and optimization suggestions for next year.
        Include total tax payable (BDT), and advice for compliance with NBR.
        """,
        expected_output="Markdown summary (Bangla + English mix)",
        agent=optimization_agent
    )

    crew = Crew(
        agents=[doc_parsing_agent, income_classifier, deduction_agent, tax_calc_agent, optimization_agent],
        tasks=[parse_task, classify_task, deduction_task, tax_task, optimize_task],
        verbose=True
    )

    result = crew.kickoff()
    final_output = str(result).strip("`")

    return JSONResponse(content={"tax_summary": final_output})
