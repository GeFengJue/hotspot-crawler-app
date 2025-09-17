from flask import Flask, jsonify, request
from flask_cors import CORS
from database_manager import DatabaseManager
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
# 添加CORS支持，允许所有来源访问
CORS(app, resources={r"/api/*": {"origins": "*"}})
db_manager = DatabaseManager()

@app.route('/')
def index():
    """首页"""
    return jsonify({
        'message': '热点数据API服务',
        'endpoints': {
            '/api/hot_news': '获取热点资讯数据',
            '/api/today_hotspot': '获取今日热点数据', 
            '/api/financial_calendar': '获取财经日历数据',
            '/api/statistics': '获取数据统计'
        }
    })

@app.route('/api/hot_news')
def get_hot_news():
    """获取热点资讯数据"""
    try:
        # 获取查询参数
        limit = request.args.get('limit', 50, type=int)
        news_type = request.args.get('type')
        
        data = db_manager.get_hot_news(limit, news_type)
        
        return jsonify({
            'success': True,
            'count': len(data),
            'data': data
        })
        
    except Exception as e:
        logging.error(f"获取热点资讯数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/today_hotspot')
def get_today_hotspot():
    """获取今日热点数据"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        data = db_manager.get_today_hotspot(limit)
        
        return jsonify({
            'success': True,
            'count': len(data),
            'data': data
        })
        
    except Exception as e:
        logging.error(f"获取今日热点数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/financial_calendar')
def get_financial_calendar():
    """获取财经日历数据"""
    try:
        limit = request.args.get('limit', 50, type=int)
        date_filter = request.args.get('date')
        
        data = db_manager.get_financial_calendar(limit, date_filter)
        
        return jsonify({
            'success': True,
            'count': len(data),
            'data': data
        })
        
    except Exception as e:
        logging.error(f"获取财经日历数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics')
def get_statistics():
    """获取数据统计"""
    try:
        stats = db_manager.get_data_statistics()
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        logging.error(f"获取数据统计失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search')
def search_data():
    """搜索数据"""
    try:
        keyword = request.args.get('q', '')
        limit = request.args.get('limit', 20, type=int)
        
        if not keyword:
            return jsonify({
                'success': False,
                'error': '请提供搜索关键词'
            }), 400
        
        # 这里可以扩展搜索功能，目前简单返回提示
        return jsonify({
            'success': True,
            'message': '搜索功能待实现',
            'keyword': keyword,
            'limit': limit
        })
        
    except Exception as e:
        logging.error(f"搜索数据失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("热点数据API服务器启动")
    print("=" * 50)
    print("API端点:")
    print("  GET /api/hot_news          - 获取热点资讯数据")
    print("  GET /api/today_hotspot      - 获取今日热点数据")
    print("  GET /api/financial_calendar - 获取财经日历数据")
    print("  GET /api/statistics         - 获取数据统计")
    print("  GET /api/search             - 搜索数据")
    print("\n服务器运行在: http://127.0.0.1:5000")
    print("按 Ctrl+C 停止服务器")
    
    app.run(debug=True, host='0.0.0.0', port=5000)