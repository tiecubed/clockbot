"""Discord Bot Entry Point"""
import os
import sys
import asyncio
import discord
from discord.ext import commands

# Add bot package to path
sys.path.insert(0, os.path.dirname(__file__))

from bot.config import config
from bot.commands.router import ClockCommandRouter


class TimeTrackerBot(commands.Bot):
    """Discord Bot for Time Tracking"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None  # Disable default help, we have our own
        )
        
        self.router: ClockCommandRouter = None
    
    async def setup_hook(self):
        """Setup bot hooks"""
        # Initialize command router
        self.router = ClockCommandRouter(self)
        
        # Register unified !clock command
        @self.command(name='clock')
        async def clock_command(ctx: commands.Context, *args):
            """Unified !clock command - routes to all subcommands"""
            await self.router.route(ctx, *args)
        
        print(f"✅ Bot initialized with unified !clock command")
    
    async def on_ready(self):
        """Called when bot is ready"""
        print(f'✅ Logged in as {self.user} (ID: {self.user.id})')
        print(f'✅ Command prefix: !clock')
        print(f'✅ Connected to {len(self.guilds)} guilds')
    
    async def on_command_error(self, ctx: commands.Context, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandNotFound):
            # Only respond to !clock, ignore other commands
            if ctx.message.content.startswith('!clock'):
                await ctx.send("❌ Unknown clock command. Type `!clock help` for usage.")
            return
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("⛔ You don't have permission to use this command.")
            return
        
        # Log other errors
        print(f"Command error: {error}")
        await ctx.send(f"❌ An error occurred: {str(error)}")
    
    async def close(self):
        """Cleanup on shutdown"""
        if self.router:
            await self.router.close()
        await super().close()


def main():
    """Main entry point"""
    # Check configuration
    if not config.is_configured:
        print("❌ Bot not configured!")
        print("Please set DISCORD_TOKEN and SHARED_TOKEN in .env file")
        sys.exit(1)
    
    # Create and run bot
    bot = TimeTrackerBot()
    
    try:
        bot.run(config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("\n👋 Bot shutting down...")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
