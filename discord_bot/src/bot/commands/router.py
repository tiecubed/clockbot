"""Unified !clock Command Router - Single entry point for all clock commands"""
import discord
from discord.ext import commands
from typing import List, Optional
from ..core.checks import ClockChecks
from ..core.api_client import BackendAPIClient
from ..services.formatter import EmbedFormatter


class ClockCommandRouter:
    """Central dispatcher for all !clock subcommands"""
    
    # Subcommand categories
    USER_COMMANDS = {'in', 'out', 'pay', 'help'}
    ADMIN_COMMANDS = {
        'hourlyrate', 'addtime', 'removetime', 
        'day', 'week', 'who', 'status',
        'setchannel', 'clear'
    }
    
    # Map subcommand names to handler method names
    COMMAND_MAP = {
        'in': 'in_',  # 'in' subcommand -> 'in_' method (Python keyword conflict)
    }
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api = BackendAPIClient()
        self.formatter = EmbedFormatter()
        
        # Import handlers
        from .user import UserCommandHandler
        from .admin import AdminCommandHandler
        
        self.user_handler = UserCommandHandler(bot, self.api, self.formatter)
        self.admin_handler = AdminCommandHandler(bot, self.api, self.formatter)
    
    def _get_method_name(self, subcommand: str) -> str:
        """Get handler method name from subcommand (handles keyword conflicts)"""
        return self.COMMAND_MAP.get(subcommand, subcommand)
    
    async def route(self, ctx: commands.Context, *args: str):
        """Main entry point - routes to appropriate handler"""
        
        # Show help if no subcommand
        if not args:
            return await self.user_handler.show_help(ctx)
        
        subcommand = args[0].lower()
        remaining_args = args[1:]
        
        # Check if admin for help display
        if subcommand == 'help':
            return await self.user_handler.show_help(ctx)
        
        # Route user commands
        if subcommand in self.USER_COMMANDS:
            handler = getattr(self.user_handler, self._get_method_name(subcommand), None)
            if handler:
                return await handler(ctx, *remaining_args)
            return await ctx.send(f"❌ Unknown user command: `{subcommand}`")
        
        # Route admin commands
        if subcommand in self.ADMIN_COMMANDS:
            # Check admin permission
            is_admin = await ClockChecks.is_admin(ctx)
            if not is_admin:
                return await ctx.send("⛔ Admin access required.")
            
            handler = getattr(self.admin_handler, subcommand, None)
            if handler:
                return await handler(ctx, *remaining_args)
            return await ctx.send(f"❌ Unknown admin command: `{subcommand}`")
        
        # Unknown command - show help
        await ctx.send(f"❌ Unknown command: `{subcommand}`")
        await self.user_handler.show_help(ctx)
    
    async def close(self):
        """Cleanup resources"""
        await self.api.close()
