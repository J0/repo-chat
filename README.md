# Repo Chat

Repo chat allows you to ask questions about a GitHub repository. This is a fork of [mckaywrigley's original repo](https://github.com/mckaywrigley/repo-chat). It uses the `vecs` adapter as well as Huggingface `supabase/gte-small` to generate embeddings. 

## Requirements

In this project we use [OpenAI embeddings](https://platform.openai.com/docs/guides/embeddings) and [Supabase with pgvector](https://supabase.com/docs/guides/database/extensions/pgvector) as our vector database.

You can switch out either of these with your own preference.

## How To Run

1. Go to [Supabase](https://supabase.com/)
2. Create your account, if you already don’t have it. 
3. Once your account is created, click on **All projects>Create Project** 
4. Copy .env.example file and rename it as .env
5. Put your project name, then go to Settings > Database >Connection Pooling Custom Configuration >Connection String to and fill in `DB_CONNECTION` with that string.
6. Now, click on your project name on Supabase, and click on the SQL Editor menu which is on the left sidebar. 
![image](images/new-query.png)
7. Configure the `.env` file with your repo url, repo branch of your choice, openai key, make sure you changed the Supabase's URL and key in the step 6.

8. Run `pip install -r requirements.txt` to install the dependencies.

9. Run the `python3 load.py` script to clone the repo.

10. Run the `python3 embed.py` script to embed the repo.

11. Run the `python3 main.py` script to ask questions about the repo.

## Contact

If you have any questions, feel free to reach out to Mckay on [Twitter](https://twitter.com/mckaywrigley)!
