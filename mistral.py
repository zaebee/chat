import os
import time
import json
from typing import Optional, Dict, Any, List
from mistralai import Mistral
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class AgentAction:
    """Действие, которое может выполнить агент"""

    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)


class HiveGardenerAgent:
    def __init__(
        self,
        env_file: str = ".env",
        model: str = "mistral-medium-2505",
        create_agent: bool = False,
    ):
        """
        Инициализация агента садовника.

        Args:
            api_key: API ключ для Mistral AI
            model: Модель Mistral AI для использования
        """
        load_dotenv(env_file)
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.agent_id = os.getenv("AGENT_ID")
        if not self.api_key:
            raise ValueError(
                "API ключ для Mistral AI не указан. Установите MISTRAL_API_KEY в переменных окружения."
            )

        self.client = Mistral(api_key=self.api_key)
        self.model = model
        self.agent = None
        self.conversation_id = None
        self.actions: Dict[str, AgentAction] = {}
        if create_agent:
            self._initialize_agent()
        self._register_default_actions()

        # Agent initialized successfully

    def _initialize_agent(self):
        """Инициализация агента на основе документации Mistral AI"""
        try:
            # Создаем агента с системным промптом
            agent = self.client.beta.agents.create(
                model=self.model,
                description="Агент садовник, который выращивает живые системы кода",
                name="HiveGardenerAgent",
                instructions=self._get_system_prompt(
                    "TODO: paste our teammate profile"
                ),
                # tools=[{"type": "function"}],  # Поддержка пользовательских функций
                completion_args={
                    "temperature": 0.3,
                    "top_p": 0.95,
                },
            )
            self.agent_id = agent.id
            # Agent created successfully
        except Exception as e:
            raise RuntimeError(f"Ошибка при создании агента: {str(e)}")

    def _get_system_prompt(self, system: str) -> str:
        """Получение системного промпта для агента"""
        return system

    def _register_default_actions(self):
        """Регистрация стандартных действий агента"""
        self.register_action(
            name="analyze_hive",
            description="Анализ состояния улья (τ, φ-метрики, Σ)",
            parameters={"depth": "Глубина анализа (basic, detailed, full)"},
        )

        self.register_action(
            name="generate_code",
            description="Генерация кода для новой пчелы",
            parameters={
                "bee_type": "Тип пчелы (A, T, C, G)",
                "name": "Имя пчелы",
                "invariants": "Список инвариантов (если применимо)",
            },
        )

        self.register_action(
            name="refactor_aggregate",
            description="Рефакторинг агрегата (A)",
            parameters={
                "aggregate_name": "Имя агрегата",
                "issues": "Список проблем (OntoPressure, HiddenCommand и т.д.)",
            },
        )

    def register_action(
        self, name: str, description: str, parameters: Dict[str, Any] | None = None
    ):
        """Регистрация нового действия для агента"""
        self.actions[name] = AgentAction(
            name=name, description=description, parameters=parameters or {}
        )

    def _execute_action(
        self, action_name: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Выполнение действия агента"""
        if action_name not in self.actions:
            raise ValueError(f"Действие {action_name} не зарегистрировано")

        # В реальном приложении здесь был бы вызов к вашей системе
        # Для демонстрации возвращаем фиктивные данные
        if action_name == "analyze_hive":
            depth = parameters.get("depth", "basic")
            analysis = {
                "τ": 0.32,
                "φ_metrics": {
                    "OntoPressure": 0.1,
                    "HiddenCommand": 0.0,
                    "EmoHook": 0.2,
                },
                "Σ": 8,
                "recommendations": [
                    "Улей в норме",
                    "Рекомендуется добавить тесты для новых модулей",
                ],
            }

            if depth == "detailed":
                analysis["code_churn"] = 25
                analysis["event_lag"] = 80
            elif depth == "full":
                analysis["test_coverage"] = 90
                analysis["critical_points"] = []

            return analysis

        elif action_name == "generate_code":
            bee_type = parameters.get("bee_type", "T")
            name = parameters.get("name", "NewBee")
            invariants = parameters.get("invariants", [])

            return {
                "bee_type": bee_type,
                "name": name,
                "invariants": invariants,
                "code_snippet": f"# {name} ({bee_type})\nclass {name}:\n    pass",
                "τ_impact": 0.02,
                "Σ_cost": 1,
            }

        elif action_name == "refactor_aggregate":
            aggregate_name = parameters.get("aggregate_name", "OrderAggregate")
            issues = parameters.get("issues", [])

            return {
                "aggregate_name": aggregate_name,
                "issues_resolved": issues,
                "changes": [
                    f"Разделение {aggregate_name} на {aggregate_name}Header и {aggregate_name}Lines",
                    "Добавление явных инвариантов",
                ],
                "τ_impact": -0.05,
                "Σ_cost": 3,
            }

        else:
            raise ValueError(f"Неизвестное действие: {action_name}")

    def _get_available_actions(self) -> str:
        """Получение списка доступных действий в формате для LLM"""
        actions_desc = []
        for action in self.actions.values():
            params = ", ".join(f"{k}: {v}" for k, v in action.parameters.items())
            actions_desc.append(
                f"- {action.name}: {action.description} (параметры: {params})"
            )

        return "\n".join(actions_desc)

    def _should_execute_action(self, response: str) -> Optional[Dict[str, Any]]:
        """Определение, нужно ли выполнять действие на основе ответа LLM"""
        try:
            # Пытаемся распарсить JSON с действием
            action_data = json.loads(response)
            if "action" in action_data and action_data["action"] in self.actions:
                return action_data
        except json.JSONDecodeError:
            pass

        return None

    def execute_conversation(self, user_input: str) -> Dict[str, Any]:
        """
        Выполнение разговора с агентом.

        Args:
            user_input: Входное сообщение пользователя

        Returns:
            Ответ агента с метаданными
        """
        try:
            if not self.conversation_id:
                # Начинаем новую беседу
                response = self.client.beta.conversations.start(
                    agent_id=self.agent_id, inputs=user_input
                )
                self.conversation_id = response.conversation_id
            else:
                # Продолжаем существующую беседу
                response = self.client.beta.conversations.append(
                    conversation_id=self.conversation_id, inputs=user_input
                )

            # Получаем полную историю беседы
            conversation_history = self.client.beta.conversations.get_history(
                conversation_id=self.conversation_id
            )
            latest = conversation_history.entries[-1]
            # Проверяем, нужно ли выполнять действие
            last_message = str(latest.content)  # type: ignore
            action_data = self._should_execute_action(last_message)

            if action_data:
                # Выполняем действие
                action_name = action_data["action"]
                action_params = action_data.get("parameters", {})

                result = self._execute_action(action_name, action_params)

                # Добавляем результат в беседу
                result_message = (
                    f"Результат выполнения {action_name}: {json.dumps(result)}"
                )
                response = self.client.beta.conversations.append(
                    conversation_id=self.conversation_id, inputs=result_message
                )

                # Формируем окончательный ответ
                final_response = f"Выполнено действие: {action_name}\nРезультат:\n{json.dumps(result, indent=2)}"
                return {
                    "response": final_response,
                    "action_executed": action_name,
                    "action_result": result,
                    "metadata": {
                        "model": self.model,
                        "timestamp": time.time(),
                        "conversation_id": self.conversation_id,
                    },
                }
            else:
                # Просто возвращаем ответ LLM
                return {
                    "response": last_message,
                    "metadata": {
                        "model": self.model,
                        "timestamp": time.time(),
                        "conversation_id": self.conversation_id,
                    },
                }

        except Exception as e:
            error_response = f"⚠ Ошибка при обращении к Mistral AI: {str(e)}"
            return {
                "response": error_response,
                "metadata": {"error": str(e), "timestamp": time.time()},
            }

    def start_interactive_session(self):
        """Запуск интерактивной сессии с агентом"""
        # Interactive session started

        while True:
            try:
                user_input = input("> ").strip()
                if user_input.lower() in ["выход", "exit", "quit"]:
                    # Session terminated
                    break

                if not user_input:
                    continue

                response = self.execute_conversation(user_input)
                # Response received

                # Если было выполнено действие, выводим дополнительную информацию
                if "action_executed" in response:
                    # Action executed with metrics

            except KeyboardInterrupt:
                # Session terminated by user
                break
            except Exception as e:
                # Error handled


if __name__ == "__main__":
    # Пример использования:
    # 1. С указанием API ключа
    # agent = HiveGardenerAgent(api_key="ваш_api_ключ")

    # 2. Через переменную окружения (рекомендуется)
    # export MISTRAL_API_KEY="ваш_api_ключ"
    # agent = HiveGardenerAgent()

    # 3. С указанием конкретной модели
    # agent = HiveGardenerAgent(model="mistral-small-latest")

    # Использует MISTRAL_API_KEY из переменных окружения
    agent = HiveGardenerAgent()
    agent.start_interactive_session()
