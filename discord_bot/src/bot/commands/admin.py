"""Admin Commands: hourlyrate, addtime, removetime, day, week, who, status, setchannel, clear"""
import discord
from discord.ext import commands
from ..core.checks import ClockChecks
from ..core.api_client import BackendAPIClient
from ..services.formatter import EmbedFormatter


class AdminCommandHandler:
    """Handles all admin-level !clock subcommands"""
    
    def __init__(self, bot: commands.Bot, api: BackendAPIClient, formatter: EmbedFormatter):
        self.bot = bot
        self.api = api
        self.formatter = formatter
    
    async def hourlyrate(self, ctx: commands.Context, *args):
        """!clock hourlyrate @user 15"""
        if len(args) < 2:
            await ctx.send("Usage: `!clock hourlyrate @user 15`")
            return
        
        # Parse mentions and rate
        user_mention = args[0]
        try:
            hourly_rate = float(args[1])
        except ValueError:
            await ctx.send("Hourly rate must be a number")
            return
        
        # Extract user ID from mention
        if not user_mention.startswith('<@') or not user_mention.endswith('>'):
            await ctx.send("Please mention a user with @")
            return
        
        user_id = user_mention.strip('<@!>')
        
        try:
            result = await self.api.set_hourly_rate(user_id, hourly_rate)
            await ctx.send(
                f"✅ Set hourly rate for {user_mention} to ${hourly_rate:.2f}/hour"
            )
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    
    async def addtime(self, ctx: commands.Context, *args):
        """!clock addtime 30 @user"""
        if len(args) < 2:
            await ctx.send("Usage: `!clock addtime 30 @user`")
            return
        
        try:
            minutes = int(args[0])
        except ValueError:
            await ctx.send("Minutes must be a number")
            return
        
        user_mention = args[1]
        if not user_mention.startswith('<@') or not user_mention.endswith('>'):
            await ctx.send("Please mention a user with @")
            return
        
        user_id = user_mention.strip('<@!>')
        reason = ' '.join(args[2:]) if len(args) > 2 else "Manual adjustment by admin"
        
        try:
            result = await self.api.add_manual_time(
                user_id, minutes, reason, str(ctx.author.id)
            )
            await ctx.send(f"✅ Added {minutes} minutes to {user_mention}")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    
    async def removetime(self, ctx: commands.Context, *args):
        """!clock removetime 30 @user"""
        if len(args) < 2:
            await ctx.send("Usage: `!clock removetime 30 @user`")
            return
        
        try:
            minutes = -int(args[0])  # Negative for removal
        except ValueError:
            await ctx.send("Minutes must be a number")
            return
        
        user_mention = args[1]
        if not user_mention.startswith('<@') or not user_mention.endswith('>'):
            await ctx.send("Please mention a user with @")
            return
        
        user_id = user_mention.strip('<@!>')
        reason = ' '.join(args[2:]) if len(args) > 2 else "Manual adjustment by admin"
        
        try:
            result = await self.api.add_manual_time(
                user_id, minutes, reason, str(ctx.author.id)
            )
            await ctx.send(f"✅ Removed {abs(minutes)} minutes from {user_mention}")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    
    async def day(self, ctx: commands.Context, *args):
        """!clock day @user"""
        await self._show_time_summary(ctx, args, 'today', 'day')
    
    async def week(self, ctx: commands.Context, *args):
        """!clock week @user"""
        await self._show_time_summary(ctx, args, 'week', 'week')
    
    async def _show_time_summary(self, ctx: commands.Context, args, endpoint: str, label: str):
        """Helper for day/week summaries"""
        if not args:
            await ctx.send(f"Usage: `!clock {label} @user`")
            return
        
        user_mention = args[0]
        if not user_mention.startswith('<@') or not user_mention.endswith('>'):
            await ctx.send("Please mention a user with @")
            return
        
        user_id = user_mention.strip('<@!>')
        
        try:
            if endpoint == 'today':
                data = await self.api.get_today_time(user_id)
            else:
                data = await self.api.get_week_time(user_id)
            
            embed = self.formatter.time_summary_embed(user_mention, data, label)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    
    async def who(self, ctx: commands.Context, *args):
        """!clock who - Show active users"""
        try:
            data = await self.api.get_active_users()
            embed = self.formatter.active_users_embed(data)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    
    async def status(self, ctx: commands.Context, *args):
        """!clock status @user"""
        if not args:
            await ctx.send("Usage: `!clock status @user`")
            return
        
        user_mention = args[0]
        if not user_mention.startswith('<@') or not user_mention.endswith('>'):
            await ctx.send("Please mention a user with @")
            return
        
        user_id = user_mention.strip('<@!>')
        
        try:
            data = await self.api.get_user_status(user_id)
            embed = self.formatter.user_status_embed(user_mention, data)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
    
    async def setchannel(self, ctx: commands.Context, *args):
        """!clock setchannel inout #channel"""
        await ctx.send("⚠️ Channel configuration - implement via bot settings")
    
    async def clear(self, ctx: commands.Context, *args):
        """!clock clear - Mark all as paid"""
        try:
            # Get unpaid summary for message
            data = await self.api.get_all_unpaid()
            users = data.get('users', [])
            
            if not users:
                await ctx.send("No unpaid time to clear.")
                return
            
            # Build payment message
            mentions = [f"<@{u['user_id']}>" for u in users]
            total = sum(u['pay_amount'] for u in users)
            
            # Clear payroll
            await self.api.clear_payroll()
            
            await ctx.send(
                f"✅ **Payroll Cleared**\n"
                f"Total paid: ${total:.2f}\n"
                f"Users paid: {', '.join(mentions)}\n"
                f"Payment of ${total:.2f} sent."
            )
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
