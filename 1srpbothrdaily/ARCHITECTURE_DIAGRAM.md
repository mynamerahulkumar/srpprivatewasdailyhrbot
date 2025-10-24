# 🏗️ Breakout Trading Bot - System Architecture

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           BREAKOUT TRADING BOT SYSTEM                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CONFIG        │    │   MAIN          │    │   BREAKOUT      │    │   DELTA        │
│   LOADER        │◄──►│   MODULE        │◄──►│   BOT ENGINE    │◄──►│   CLIENT       │
│                 │    │                 │    │                 │    │                 │
│ • YAML Config   │    │ • Entry Point   │    │ • Trading Logic │    │ • API Client    │
│ • Validation    │    │ • Error Handling │    │ • Risk Mgmt     │    │ • Authentication│
│ • Credentials   │    │ • Logging Setup  │    │ • Position Mgmt │    │ • Order Mgmt    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         │                       │                       │                       │
         ▼                       ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CONFIG        │    │   LOGGING       │    │   POSITION      │    │   DELTA         │
│   FILES         │    │   SYSTEM        │    │   MONITORING    │    │   EXCHANGE      │
│                 │    │                 │    │                 │    │   API           │
│ • config.yaml   │    │ • File Logging  │    │ • P&L Calc      │    │                 │
│ • .env          │    │ • Console Log   │    │ • Breakeven     │    │ • Market Data  │
│ • env.example   │    │ • Error Tracking│    │ • Risk Checks   │    │ • Order Execution│
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Detailed Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              COMPONENT DETAILS                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                CONFIG LOADER                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Purpose: Configuration Management and Validation                               │
│  Files: config_loader.py (188 lines)                                          │
│                                                                                 │
│  Key Methods:                                                                   │
│  ├─ get_trading_config() → Trading parameters                                   │
│  ├─ get_schedule_config() → Time and timeframe settings                        │
│  ├─ get_risk_config() → Risk management settings                               │
│  ├─ get_api_credentials() → API keys and secrets                                │
│  └─ get_monitoring_config() → Monitoring intervals                             │
│                                                                                 │
│  Input: config.yaml, .env files                                                │
│  Output: Validated configuration objects                                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DELTA EXCHANGE CLIENT                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Purpose: API Communication and Trading Operations                             │
│  Files: delta_client.py (431 lines)                                            │
│                                                                                 │
│  Key Methods:                                                                   │
│  ├─ get_historical_candles() → OHLCV data retrieval                            │
│  ├─ get_ticker() → Current market prices                                       │
│  ├─ place_limit_order() → Order placement                                      │
│  ├─ get_positions() → Position monitoring                                       │
│  ├─ cancel_order() → Order cancellation                                        │
│  └─ edit_order() → Order modification                                          │
│                                                                                 │
│  Authentication: HMAC SHA256 signature                                         │
│  Rate Limiting: 100 requests/minute, 1000 requests/hour                          │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BREAKOUT BOT ENGINE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Purpose: Core Trading Logic and Strategy Implementation                       │
│  Files: breakout_bot.py (992 lines)                                           │
│                                                                                 │
│  Key Methods:                                                                   │
│  ├─ calculate_previous_period_levels() → High/Low calculation                   │
│  ├─ place_breakout_orders() → Order placement logic                           │
│  ├─ monitor_position_and_apply_breakeven() → Risk management                   │
│  ├─ check_position_closed() → Position monitoring                             │
│  └─ perform_reset() → Periodic strategy reset                                  │
│                                                                                 │
│  State Management:                                                              │
│  ├─ Position tracking (entry, side, size)                                      │
│  ├─ Order management (buy/sell order IDs)                                      │
│  ├─ Risk management (SL/TP orders)                                            │
│  └─ Breakeven logic (profit protection)                                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                MAIN MODULE                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Purpose: Application Entry Point and Coordination                             │
│  Files: main.py (156 lines)                                                   │
│                                                                                 │
│  Key Functions:                                                                 │
│  ├─ setup_logging() → Logging configuration                                    │
│  ├─ main() → Application entry point                                           │
│  └─ Component initialization and error handling                                │
│                                                                                 │
│  Flow:                                                                          │
│  ├─ Load configuration                                                         │
│  ├─ Initialize API client                                                       │
│  ├─ Test API connection                                                         │
│  ├─ Initialize trading bot                                                      │
│  └─ Start main trading loop                                                    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                DATA FLOW                                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CONFIG        │    │   INITIALIZATION│    │   DATA          │    │   TRADING       │
│   PHASE         │    │   PHASE         │    │   COLLECTION    │    │   PHASE         │
│                 │    │                 │    │   PHASE         │    │                 │
│ 1. Load YAML   │───►│ 2. Setup Logging│───►│ 3. Fetch Market │───►│ 4. Calculate    │
│    config       │    │    system        │    │    data         │    │    levels       │
│                 │    │                 │    │                 │    │                 │
│ 2. Load API    │    │ 3. Initialize   │    │ 4. Get historical│    │ 5. Place orders │
│    credentials  │    │    Delta client │    │    candles      │    │                 │
│                 │    │                 │    │                 │    │                 │
│ 3. Validate    │    │ 4. Test API     │    │ 5. Calculate     │    │ 6. Monitor      │
│    parameters   │    │    connection    │    │    high/low      │    │    positions    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         │                       │                       │                       │
         ▼                       ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MONITORING    │    │   RISK          │    │   POSITION      │    │   RESET         │
│   PHASE         │    │   MANAGEMENT    │    │   MANAGEMENT    │    │   PHASE         │
│                 │    │                 │    │                 │    │                 │
│ 5. Check order  │    │ 6. Calculate    │    │ 7. Track P&L    │    │ 8. Cancel old   │
│    status       │    │    P&L          │    │    continuously │    │    orders       │
│                 │    │                 │    │                 │    │                 │
│ 6. Monitor      │    │ 7. Check       │    │ 8. Apply        │    │ 9. Calculate    │
│    positions    │    │    breakeven    │    │    breakeven     │    │    new levels    │
│                 │    │    trigger      │    │    logic         │    │                 │
│ 7. Handle       │    │ 8. Move SL to   │    │ 9. Detect       │    │ 10. Place new   │
│    errors       │    │    entry        │    │    position     │    │    orders        │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## API Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            API INTEGRATION LAYER                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DELTA EXCHANGE API                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Base URL: https://api.india.delta.exchange                                    │
│  Authentication: HMAC SHA256                                                   │
│  Rate Limits: 100 req/min, 1000 req/hour                                       │
│                                                                                 │
│  Endpoints:                                                                     │
│  ├─ GET  /v2/history/candles    → Historical OHLCV data                        │
│  ├─ GET  /v2/tickers/{symbol}   → Current market prices                       │
│  ├─ POST /v2/orders              → Place orders                               │
│  ├─ GET  /v2/orders              → Get open orders                            │
│  ├─ GET  /v2/positions           → Get positions                               │
│  ├─ PUT  /v2/orders              → Edit orders                                 │
│  └─ DELETE /v2/orders            → Cancel orders                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT WRAPPER                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Purpose: Simplify API interactions and handle errors                          │
│                                                                                 │
│  Features:                                                                      │
│  ├─ Automatic authentication (HMAC SHA256)                                     │
│  ├─ Request/response logging                                                   │
│  ├─ Error handling and retries                                                 │
│  ├─ Rate limiting compliance                                                   │
│  └─ Type-safe method signatures                                                │
│                                                                                 │
│  Method Categories:                                                             │
│  ├─ Market Data Methods                                                         │
│  │  ├─ get_historical_candles()                                                 │
│  │  └─ get_ticker()                                                            │
│  ├─ Trading Methods                                                             │
│  │  ├─ place_limit_order()                                                     │
│  │  ├─ edit_order()                                                            │
│  │  └─ cancel_order()                                                          │
│  └─ Monitoring Methods                                                          │
│      ├─ get_positions()                                                         │
│      └─ get_open_orders()                                                      │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## State Management Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              STATE MANAGEMENT                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              BOT STATE MACHINE                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   WAITING   │    │ CALCULATING │    │   ORDERS    │    │  POSITION   │      │
│  │  FOR RESET  │───►│   LEVELS    │───►│   PLACED    │───►│    OPEN     │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│         ▲                   │                   │                   │         │
│         │                   │                   │                   │         │
│         │                   ▼                   ▼                   ▼         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   POSITION │    │   BREAKEVEN │    │   POSITION  │    │   POSITION  │      │
│  │   CLOSED   │◄───│   APPLIED   │◄───│  MONITORING │◄───│   OPEN      │      │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                                                 │
│  State Transitions:                                                             │
│  ├─ WAITING → CALCULATING: Time trigger (reset interval)                       │
│  ├─ CALCULATING → ORDERS: Levels calculated successfully                       │
│  ├─ ORDERS → POSITION: One order filled                                       │
│  ├─ POSITION → MONITORING: Position opened                                    │
│  ├─ MONITORING → BREAKEVEN: Profit threshold reached                          │
│  └─ POSITION → CLOSED: SL/TP hit or manual close                             │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA STRUCTURES                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Bot State Variables:                                                          │
│  ├─ prev_period_high: float        → Previous period high price               │
│  ├─ prev_period_low: float         → Previous period low price                │
│  ├─ buy_order_id: int              → Buy order ID                             │
│  ├─ sell_order_id: int             → Sell order ID                            │
│  ├─ active_position: dict           → Current position data                    │
│  ├─ entry_price: float             → Position entry price                     │
│  ├─ position_side: str             → 'long' or 'short'                        │
│  ├─ breakeven_applied: bool        → Breakeven status                         │
│  ├─ stop_loss_order_id: int        → Stop loss order ID                       │
│  └─ take_profit_order_id: int      → Take profit order ID                     │
│                                                                                 │
│  Configuration Objects:                                                        │
│  ├─ trading_config: dict           → Trading parameters                        │
│  ├─ schedule_config: dict          → Time and timeframe settings              │
│  ├─ risk_config: dict              → Risk management settings                 │
│  └─ monitoring_config: dict        → Monitoring intervals                     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Error Handling Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ERROR HANDLING                                     │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ERROR CATEGORIES                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. CONFIGURATION ERRORS                                                       │
│     ├─ Missing config files                                                     │
│     ├─ Invalid YAML syntax                                                     │
│     ├─ Missing API credentials                                                  │
│     └─ Invalid parameter values                                                 │
│                                                                                 │
│  2. API ERRORS                                                                  │
│     ├─ Authentication failures                                                 │
│     ├─ Network timeouts                                                        │
│     ├─ Rate limit exceeded                                                     │
│     └─ Invalid API responses                                                   │
│                                                                                 │
│  3. TRADING ERRORS                                                             │
│     ├─ Insufficient balance                                                    │
│     ├─ Invalid order parameters                                                │
│     ├─ Order placement failures                                                │
│     └─ Position monitoring errors                                               │
│                                                                                 │
│  4. SYSTEM ERRORS                                                              │
│     ├─ Memory issues                                                           │
│     ├─ Disk space problems                                                     │
│     ├─ Process crashes                                                         │
│     └─ External dependencies                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ERROR HANDLING STRATEGY                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Error Detection:                                                              │
│  ├─ Try-catch blocks around critical operations                               │
│  ├─ API response validation                                                     │
│  ├─ State consistency checks                                                    │
│  └─ Timeout monitoring                                                          │
│                                                                                 │
│  Error Recovery:                                                                │
│  ├─ Automatic retries with exponential backoff                                 │
│  ├─ Fallback to safe states                                                    │
│  ├─ Graceful degradation                                                       │
│  └─ Emergency stop procedures                                                   │
│                                                                                 │
│  Error Reporting:                                                               │
│  ├─ Detailed logging with context                                               │
│  ├─ Error classification and severity                                            │
│  ├─ Performance impact assessment                                               │
│  └─ Recovery action logging                                                     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Testing Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              TESTING FRAMEWORK                                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              TEST CATEGORIES                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  1. UNIT TESTS (32 tests)                                                      │
│     ├─ ConfigLoader Tests (9 tests)                                            │
│     │  ├─ Configuration loading                                                 │
│     │  ├─ Parameter validation                                                  │
│     │  ├─ Error handling                                                       │
│     │  └─ Type safety                                                          │
│     ├─ DeltaClient Tests (17 tests)                                            │
│     │  ├─ API authentication                                                   │
│     │  ├─ Request/response handling                                            │
│     │  ├─ Error scenarios                                                      │
│     │  └─ Rate limiting                                                        │
│     └─ BreakoutBot Tests (6 tests)                                             │
│         ├─ Level calculation                                                    │
│         ├─ Order placement logic                                                │
│         ├─ Position monitoring                                                  │
│         └─ State management                                                    │
│                                                                                 │
│  2. INTEGRATION TESTS (10 tests)                                               │
│     ├─ Breakout Logic Tests                                                    │
│     │  ├─ Multi-timeframe support                                              │
│     │  ├─ Strategy implementation                                               │
│     │  └─ Risk management integration                                          │
│     └─ Timeframe Tests                                                          │
│         ├─ 1H, 4H, 1D timeframes                                               │
│         ├─ Reset interval calculation                                           │
│         └─ Candle timing                                                       │
│                                                                                 │
│  3. END-TO-END TESTS (6 tests)                                                 │
│     ├─ Complete trading cycle                                                  │
│     ├─ Error recovery scenarios                                                │
│     ├─ Position recovery on restart                                            │
│     └─ Multi-bot coordination                                                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              TEST DATA MANAGEMENT                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Mock Data Structure:                                                           │
│  ├─ Historical Candles:                                                        │
│  │  ├─ OHLCV data with realistic values                                         │
│  │  ├─ Multiple timeframes (1H, 4H, 1D)                                        │
│  │  └─ Edge cases (gaps, weekends)                                             │
│  ├─ API Responses:                                                             │
│  │  ├─ Successful order placement                                               │
│  │  ├─ Position data                                                           │
│  │  ├─ Error responses                                                         │
│  │  └─ Rate limit scenarios                                                    │
│  └─ Market Conditions:                                                        │
│      ├─ Trending markets                                                       │
│      ├─ Sideways markets                                                       │
│      ├─ High volatility                                                        │
│      └─ Low liquidity                                                          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DEPLOYMENT OPTIONS                                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                               LOCAL DEPLOYMENT                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Requirements:                                                                  │
│  ├─ Python 3.12+                                                               │
│  ├─ UV package manager (recommended)                                          │
│  ├─ Delta Exchange API credentials                                              │
│  └─ Stable internet connection                                                 │
│                                                                                 │
│  Setup:                                                                         │
│  ├─ Clone repository                                                            │
│  ├─ Install dependencies: uv sync                                              │
│  ├─ Configure config.yaml                                                       │
│  ├─ Setup .env with API credentials                                            │
│  └─ Run: uv run python -m src.main                                             │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AWS EC2 DEPLOYMENT                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Instance Type: t4g.micro (ARM-based)                                          │
│  Cost: ~$3.50/month (67% savings vs x86)                                       │
│                                                                                 │
│  Setup:                                                                         │
│  ├─ Launch EC2 instance (Ubuntu 22.04 ARM)                                      │
│  ├─ Install Python 3.12 and UV                                                 │
│  ├─ Clone repository                                                            │
│  ├─ Configure systemd service                                                   │
│  ├─ Setup log rotation                                                          │
│  └─ Enable auto-start on boot                                                  │
│                                                                                 │
│  Monitoring:                                                                    │
│  ├─ CloudWatch logs integration                                                 │
│  ├─ Health check endpoints                                                     │
│  ├─ Automated restarts                                                         │
│  └─ Performance monitoring                                                     │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DOCKER DEPLOYMENT                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  Dockerfile:                                                                   │
│  ├─ Python 3.12 slim base image                                                │
│  ├─ UV package manager                                                          │
│  ├─ Application code                                                            │
│  └─ Health check configuration                                                  │
│                                                                                 │
│  Docker Compose:                                                               │
│  ├─ Application service                                                         │
│  ├─ Log volume mounting                                                         │
│  ├─ Environment variable injection                                             │
│  └─ Restart policies                                                            │
│                                                                                 │
│  Benefits:                                                                      │
│  ├─ Consistent environment                                                      │
│  ├─ Easy scaling                                                                │
│  ├─ Simplified deployment                                                       │
│  └─ Resource isolation                                                          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary

This architecture provides:

1. **Modular Design**: Clear separation of concerns
2. **Scalability**: Easy to extend and modify
3. **Reliability**: Comprehensive error handling
4. **Testability**: Full test coverage
5. **Maintainability**: Clean code structure
6. **Performance**: Optimized for trading operations

The system is designed to be:
- **Production-ready**: Robust error handling and logging
- **Educational**: Clear structure for learning
- **Extensible**: Easy to add new features
- **Reliable**: Comprehensive testing and monitoring
