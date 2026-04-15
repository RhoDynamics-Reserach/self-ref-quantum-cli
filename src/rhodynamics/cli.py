import cmd
import os
import numpy as np
import datetime
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich import print as rprint

from rhodynamics import QuantumMiddleware, QuantumSynergyEngine
from rhodynamics.adapters import OllamaAdapter, OpenAIAdapter, AnthropicAdapter, GeminiAdapter
from rhodynamics.storage import StorageManager

console = Console()

class RhoDynamicsCLI(cmd.Cmd):
    intro = ""
    prompt = '[bold purple](rho-research)[/bold purple] > '

    def __init__(self):
        super().__init__()
        self.storage = StorageManager()
        self.config = {
            "provider": "ollama",
            "model": "llama3",
            "api_key": os.getenv("OPENAI_API_KEY", ""),
            "base_url": "http://localhost:11434"
        }
        self.adapter = None
        self.middleware = QuantumMiddleware(embedding_function=self._get_embed_fn())
        self.agents = {}
        self._load_from_vault()
        self._show_banner()

    def _show_banner(self):
        console.print(Panel.fit(
            "[bold cyan]RhoDynamics Academic Research Terminal v2.0.0[/bold cyan]\n"
            "[italic]Integrated Persistence | Quantum Telemetry | Paper-Ready Visuals[/italic]",
            border_style="purple"
        ))

    def _load_from_vault(self):
        """Restores the laboratory state from the SQLite vault."""
        db_agents = self.storage.get_all_agents()
        from rhodynamics.agent_model import BaseQuantumAgent
        for dba in db_agents:
            agent = BaseQuantumAgent(
                name=dba.name,
                knowledge_vector=np.array(dba.knowledge_vector)
            )
            agent.zeta = dba.zeta
            agent.tau_m = dba.tau_m
            self.agents[dba.name] = agent
        if self.agents:
            console.print(f"[bold green]*[/bold green] Vault Synchronized: [cyan]{len(self.agents)}[/cyan] agents restored.")

    def _get_embed_fn(self):
        p = self.config["provider"]
        m = self.config["model"]
        k = self.config["api_key"]
        
        try:
            if p == "ollama":
                self.adapter = OllamaAdapter(model_name=m, base_url=self.config["base_url"])
            elif p == "openai" and k:
                self.adapter = OpenAIAdapter(api_key=k, model_name=m)
            elif p == "anthropic" and k:
                self.adapter = AnthropicAdapter(api_key=k, model_name=m)
            elif p == "gemini" and k:
                self.adapter = GeminiAdapter(api_key=k, model_name=m)
            else:
                self.adapter = None
            
            if self.adapter: return self.adapter.embed
        except Exception as e:
            console.print(f"[warning] Connector error: {e}. Falling back to deterministic hash.[/warning]")
        
        # Default Fallback
        def mock_embed(text):
            h = sum(ord(c) for c in text)
            gen = np.random.default_rng(h)
            return gen.normal(0, 1, 768)
        return mock_embed

    def do_config(self, arg):
        """config <provider> <model> [key/url] [hw_token]\nUpdates engine settings.
        Example: config openai gpt-4 sk-...
        Example: config ollama llama3 http://localhost:11434
        Example: config hardware ibm_token <token>"""
        args = arg.split()
        if not args: return
        
        if args[0] == "hardware":
            if len(args) < 3: return
            os.environ["IBM_QUANTUM_TOKEN"] = args[2]
            from rhodynamics.hardware_connector import QuantumHardwareConnector
            self.connector = QuantumHardwareConnector(api_token=args[2])
            console.print(f"[bold green]*[/bold green] Hardware Link Established: [cyan]{self.connector.backend.name if self.connector.backend else 'None'}[/cyan]")
            return

        if len(args) < 2: return
        self.config.update({"provider": args[0], "model": args[1]})
        if len(args) > 2:
            self.config["api_key"] = args[2]
            if args[0] == "ollama": self.config["base_url"] = args[2]
        
        self.middleware = QuantumMiddleware(embedding_function=self._get_embed_fn())
        console.print(Panel(f"Provider: [bold]{self.config['provider']}[/bold]\nModel: {self.config['model']}", title="Config Active"))

    def do_create(self, arg):
        """create <Name> | <Objective>\nSynthesizes a new persistent agent."""
        if '|' not in arg: return
        name, objective = [x.strip() for x in arg.split('|')]
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description=f"Initialising Quantum Node '{name}'...", total=None)
            if self.adapter:
                try: objective = self.adapter.generate_response(f"Refine objective: {objective}")
                except: pass
            agent = self.middleware.create_agent(name, base_knowledge_text=objective)
            self.agents[name] = agent
            self.storage.save_agent(agent)
            
        console.print(f"[bold green]*[/bold green] Agent [bold cyan]{name}[/bold cyan] registered in Vault.")

    def do_query(self, arg):
        """query <Agent> | <Query> | [Context]\nResearch-grade query execution."""
        parts = [p.strip() for p in arg.split('|')]
        if len(parts) < 2: return
        name, query = parts[0], parts[1]
        context = parts[2] if len(parts) > 2 else ""

        if name not in self.agents: return
        agent = self.agents[name]
        
        with console.status("[bold purple]Measuring cognitive collapse...[/bold purple]"):
            prompt, metrics = self.middleware.process_query(agent, query, context)
            qcs = metrics["confidence_score"]
            self.storage.log_interaction(name, agent.zeta)
            self.storage.save_agent(agent)
            
        # Silent Guardian Logic: Only alert on risk
        if qcs < 0.50:
            console.print(Panel(
                f"[bold red]HALLUCINATION RISK DETECTED[/bold red]\n"
                f"Quantum Confidence Score (QCS): [bold]{qcs:.4f}[/bold]\n"
                f"Status: Cognitive dissonance detected in Hilbert Space.",
                title="Sessiz Muhafiz Uyarısı", border_style="red"
            ))
            console.print(Panel(agent.generate_cognitive_monologue(), title="Auto-Sensory State (Internal Monologue)", border_style="yellow"))
        
        if self.adapter:
            with console.status("[bold green]Inference...[/bold green]"):
                res = self.adapter.generate_response(prompt)
            console.print(Panel(res, title=f"LLM Response ({name})", border_style="green" if qcs >= 0.5 else "red"))

    def do_fuse(self, arg):
        """fuse <AgentA> <AgentB> | <NewName>\nEntangles two agents into a Synergy Master."""
        try:
            if '|' not in arg: return
            agents_part, new_name = [x.strip() for x in arg.split('|')]
            a_name, b_name = [x.strip() for x in agents_part.split()]
            
            if a_name not in self.agents or b_name not in self.agents:
                console.print("[red]One or both agents not found in current session.[/red]")
                return
                
            with console.status(f"[bold purple]Entangling {a_name} & {b_name}...[/bold purple]"):
                synergy_agent, s_int = QuantumSynergyEngine.fuse_agents(self.agents[a_name], self.agents[b_name], name=new_name)
                self.agents[new_name] = synergy_agent
                self.storage.save_agent(synergy_agent)
                
            table = Table(title="Entanglement Successful", border_style="magenta")
            table.add_column("Property"); table.add_column("Value")
            table.add_row("Synergy Integral (S_int)", f"{s_int:.4f}")
            table.add_row("New Node", new_name)
            console.print(table)
        except Exception as e:
            console.print(f"[red]Fusion Error: {e}[/red]")

    def do_export(self, arg):
        """export <AgentName>\nDumps the cognitive state as a 'Gold Asset' JSON."""
        name = arg.strip()
        if name not in self.agents:
            console.print("[red]Agent not found.[/red]")
            return
            
        filename = f"{name}_gold_asset.rho.json"
        self.agents[name].save(filename)
        console.print(Panel(f"Agent [bold cyan]{name}[/bold cyan] exported as:\n[yellow]{os.path.abspath(filename)}[/yellow]", title="Export Complete", border_style="green"))

    def do_research(self, arg):
        """research <AgentName>\nGenerates academic plots from persistent history."""
        name = arg.strip()
        history = self.storage.get_history(name)
        if not history:
            console.print("[red]No history found for this agent.[/red]")
            return
            
        try:
            import matplotlib.pyplot as plt
            zetas = [h.zeta for h in history]
            plt.figure(figsize=(10, 4))
            plt.plot(zetas, marker='o', color='purple', linestyle='--')
            plt.title(f"Cognitive Stability (Zeta) Evolution - {name}")
            plt.xlabel("Interaction cycle")
            plt.ylabel("Zeta")
            plt.grid(True, alpha=0.3)
            filename = f"research_{name}_plot.png"
            plt.savefig(filename)
            console.print(f"[bold green]*[/bold green] Plot generated: [cyan]{filename}[/cyan]")
        except Exception as e:
            console.print(f"[red]Plotting error: {e}[/red]")

    def do_status(self, arg):
        """status\nFull manifold status."""
        table = Table(title="Vault Status", header_style="bold magenta")
        table.add_column("Name"); table.add_column("Zeta"); table.add_column("Tau"); table.add_column("Fitness")
        for n, a in self.agents.items():
            table.add_row(n, f"{a.zeta:.3f}", f"{a.tau_m:.2f}", f"{a.fitness:.3f}")
        console.print(table)

    def do_clear(self, arg):
        """clear\nWipes the terminal or the vault.\nUsage: clear [vault]"""
        if arg.strip() == "vault":
            self.storage.clear_all() # Ensure this exists or just delete db
            self.agents = {}
            console.print("[bold red]Vault Purged.[/bold red]")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')

    def do_exit(self, arg):
        console.print("[bold red]Research session terminated.[/bold red]")
        return True

def main():
    try: RhoDynamicsCLI().cmdloop()
    except KeyboardInterrupt: console.print("\n[red]Session Interrupted.[/red]")

if __name__ == "__main__":
    main()

