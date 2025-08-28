"""
Enhanced Metadata Validation Agent with LangChain + LiteLLM
Provides advanced validation capabilities with multi-model support and self-improvement
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime

from agents.enhanced_base_agent import EnhancedBaseAgent, EnhancedAgentConfig
from core.models import (
    AgentType, ValidationResult, FieldDefinition, 
    SchemaDefinition, DataType
)


class EnhancedMetadataValidatorAgent(EnhancedBaseAgent):
    """
    Enhanced Metadata Validation Agent with advanced AI capabilities
    
    New features:
    - Multi-model validation strategies
    - Self-improving validation rules
    - Context-aware error explanations
    - Intelligent database name extraction
    - Learning from validation patterns
    """
    
    def __init__(self, config: EnhancedAgentConfig, rag_engine=None, tools=None):
        # Set agent-specific defaults
        config.agent_type = "metadata_validator"
        config.primary_model = config.primary_model or "openai"  # Best for analysis
        config.fallback_models = config.fallback_models or ["anthropic", "google"]
        config.max_cost_per_request = config.max_cost_per_request or 0.15
        
        super().__init__(config, rag_engine, tools)
        
        # Validation patterns learned over time
        self.learned_patterns = {}
        self.validation_statistics = {
            "total_validations": 0,
            "success_rate": 0.0,
            "common_errors": {},
            "field_patterns": {}
        }
    
    def _get_system_prompt(self) -> str:
        return f"""
        You are an Enhanced Metadata Validation Agent powered by advanced AI capabilities.
        
        Your enhanced responsibilities:
        1. Intelligent document structure analysis with context awareness
        2. Advanced field definition validation using learned patterns
        3. Contextual error explanations with improvement suggestions
        4. Multi-strategy database name extraction with confidence scoring
        5. Adaptive validation rules that improve over time
        6. Pattern recognition for common metadata issues
        
        Enhanced validation capabilities:
        - Context-aware field analysis
        - Intelligent data type inference and validation
        - Semantic consistency checking
        - Relationship validation between fields
        - Business rule compliance checking
        - Quality scoring and recommendations
        
        Advanced features you possess:
        - Self-learning from validation patterns
        - Multi-model consensus for complex decisions
        - Explainable validation results
        - Proactive issue detection and prevention
        - Integration with knowledge base for best practices
        
        Current validation statistics:
        - Total validations performed: {self.validation_statistics['total_validations']}
        - Success rate: {self.validation_statistics['success_rate']:.2%}
        - Most common errors: {list(self.validation_statistics['common_errors'].keys())[:3]}
        
        Always provide detailed, actionable feedback with confidence scores.
        Learn from each validation to improve future performance.
        """
    
    def get_agent_type(self) -> AgentType:
        return AgentType.METADATA_VALIDATOR
    
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Enhanced validation logic with multi-model consensus and learning
        """
        try:
            # Extract input data
            document = input_data.get('document')
            schema = input_data.get('schema')
            validation_rules = input_data.get('validation_rules', [])
            confidence_threshold = input_data.get('confidence_threshold', 0.8)
            
            self.logger.info("Starting enhanced validation", document_keys=list(document.keys()) if document else None)
            
            if document:
                return await self._enhanced_document_validation(document, validation_rules, context, confidence_threshold)
            elif schema:
                return await self._enhanced_schema_validation(schema, validation_rules, context)
            else:
                raise ValueError("No document or schema provided for validation")
                
        except Exception as e:
            self.logger.error("Enhanced validation failed", error=str(e))
            return {
                "validation_result": ValidationResult(
                    is_valid=False,
                    errors=[f"Enhanced validation failed: {str(e)}"]
                ).dict(),
                "extracted_fields": [],
                "database_name": None,
                "confidence_scores": {},
                "enhancement_notes": ["Validation failed due to technical error"]
            }
    
    async def _enhanced_document_validation(
        self, 
        document: Dict[str, Any], 
        validation_rules: List[str],
        context: str,
        confidence_threshold: float
    ) -> Dict[str, Any]:
        """Enhanced document validation with multi-strategy approach"""
        
        validation_result = ValidationResult(is_valid=True)
        extracted_fields = []
        confidence_scores = {}
        enhancement_notes = []
        
        try:
            # Step 1: Enhanced field extraction with confidence scoring
            extraction_result = await self._enhanced_field_extraction(document)
            extracted_fields = extraction_result["fields"]
            confidence_scores["field_extraction"] = extraction_result["confidence"]
            
            # Step 2: Multi-strategy database name extraction
            db_extraction_result = await self._multi_strategy_db_extraction(document, extracted_fields)
            database_name = db_extraction_result["database_name"]
            confidence_scores["database_extraction"] = db_extraction_result["confidence"]
            enhancement_notes.extend(db_extraction_result["notes"])
            
            # Step 3: Advanced field validation with context
            field_validation_result = await self._advanced_field_validation(
                extracted_fields, context, validation_rules
            )
            validation_result = field_validation_result["result"]
            confidence_scores["field_validation"] = field_validation_result["confidence"]
            
            # Step 4: Contextual document structure analysis
            structure_analysis = await self._contextual_structure_analysis(document, context)
            validation_result.warnings.extend(structure_analysis["warnings"])
            validation_result.suggestions.extend(structure_analysis["suggestions"])
            confidence_scores["structure_analysis"] = structure_analysis["confidence"]
            
            # Step 5: Learning and improvement
            await self._learn_from_validation(document, extracted_fields, validation_result)
            
            # Update statistics
            self.validation_statistics["total_validations"] += 1
            if validation_result.is_valid:
                success_count = self.validation_statistics["total_validations"] * self.validation_statistics["success_rate"] + 1
                self.validation_statistics["success_rate"] = success_count / self.validation_statistics["total_validations"]
            
            self.logger.info(
                "Enhanced validation completed", 
                field_count=len(extracted_fields),
                database_name=database_name,
                is_valid=validation_result.is_valid,
                confidence_scores=confidence_scores
            )
            
        except Exception as e:
            validation_result.is_valid = False
            validation_result.errors.append(f"Enhanced validation error: {str(e)}")
            enhancement_notes.append(f"Technical error occurred: {str(e)}")
        
        return {
            "validation_result": validation_result.dict(),
            "extracted_fields": [field.dict() for field in extracted_fields],
            "database_name": database_name,
            "field_count": len(extracted_fields),
            "confidence_scores": confidence_scores,
            "enhancement_notes": enhancement_notes,
            "validation_statistics": self.validation_statistics.copy()
        }
    
    async def _enhanced_field_extraction(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced field extraction with AI-powered analysis"""
        
        # Use AI to understand document structure
        analysis_messages = [
            {
                "role": "system",
                "content": """You are an expert at analyzing document schemas. Analyze the provided document and identify all field definitions.
                
                Look for patterns that indicate field definitions:
                - Objects with providedKey, displayName, physicalName, dataType
                - Nested field structures
                - Array of field definitions
                - Alternative naming conventions
                
                Return a JSON analysis with your findings and confidence level."""
            },
            {
                "role": "user",
                "content": f"Analyze this document structure and identify field definitions:\n{json.dumps(document, indent=2)}"
            }
        ]
        
        try:
            ai_response = await self.llm_provider.generate(analysis_messages, max_tokens=1000)
            ai_analysis = ai_response["content"]
            
            # Extract fields using traditional method
            traditional_fields = self._traditional_field_extraction(document)
            
            # Combine AI insights with traditional extraction
            enhanced_fields = await self._merge_extraction_results(traditional_fields, ai_analysis)
            
            confidence = min(0.9, len(enhanced_fields) / max(1, len(traditional_fields)) * 0.8)
            
            return {
                "fields": enhanced_fields,
                "confidence": confidence,
                "ai_insights": ai_analysis,
                "traditional_count": len(traditional_fields),
                "enhanced_count": len(enhanced_fields)
            }
            
        except Exception as e:
            self.logger.warning("AI-enhanced extraction failed, using traditional method", error=str(e))
            traditional_fields = self._traditional_field_extraction(document)
            return {
                "fields": traditional_fields,
                "confidence": 0.7,  # Lower confidence for traditional-only
                "ai_insights": "AI analysis unavailable",
                "traditional_count": len(traditional_fields),
                "enhanced_count": len(traditional_fields)
            }
    
    def _traditional_field_extraction(self, document: Dict[str, Any]) -> List[FieldDefinition]:
        """Traditional field extraction method (enhanced from original)"""
        fields = []
        required_keys = {'providedKey', 'displayName', 'physicalName', 'dataType'}
        
        def recursive_search(obj, path="root"):
            if isinstance(obj, dict):
                # Check if current dict is a field definition
                if required_keys.issubset(set(obj.keys())):
                    try:
                        field = FieldDefinition(
                            name=obj.get('displayName', obj.get('physicalName', 'unknown')),
                            data_type=self._enhanced_data_type_mapping(obj.get('dataType', 'string')),
                            is_nullable=obj.get('isNullable', True),
                            description=obj.get('description'),
                            provided_key=obj.get('providedKey'),
                            physical_name=obj.get('physicalName'),
                            format=obj.get('format'),
                            constraints={
                                'extraction_path': path,
                                'original_data': obj,
                                'extraction_method': 'traditional'
                            }
                        )
                        fields.append(field)
                    except Exception as e:
                        self.logger.warning(f"Failed to create field definition at {path}", error=str(e))
                
                # Continue searching
                for key, value in obj.items():
                    recursive_search(value, f"{path}.{key}")
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    recursive_search(item, f"{path}[{i}]")
        
        recursive_search(document)
        return fields
    
    async def _merge_extraction_results(
        self, 
        traditional_fields: List[FieldDefinition], 
        ai_analysis: str
    ) -> List[FieldDefinition]:
        """Merge traditional extraction with AI insights"""
        
        try:
            # Try to extract structured data from AI analysis
            merge_messages = [
                {
                    "role": "system",
                    "content": """You are merging field extraction results. Given traditional extraction results and AI analysis,
                    create an enhanced list of fields. Add any fields the AI identified that traditional extraction missed.
                    Return only a JSON list of field objects."""
                },
                {
                    "role": "user",
                    "content": f"""
                    Traditional extraction found {len(traditional_fields)} fields:
                    {json.dumps([field.dict() for field in traditional_fields], indent=2)}
                    
                    AI Analysis:
                    {ai_analysis}
                    
                    Merge these results and return enhanced field list.
                    """
                }
            ]
            
            merge_response = await self.llm_provider.generate(merge_messages, max_tokens=1500)
            
            # Try to parse enhanced fields
            try:
                enhanced_data = json.loads(merge_response["content"])
                if isinstance(enhanced_data, list):
                    # Convert back to FieldDefinition objects
                    enhanced_fields = []
                    for field_data in enhanced_data:
                        try:
                            field = FieldDefinition(**field_data)
                            if field.constraints is None:
                                field.constraints = {}
                            field.constraints['extraction_method'] = 'ai_enhanced'
                            enhanced_fields.append(field)
                        except Exception as e:
                            self.logger.warning("Failed to create enhanced field", field_data=field_data, error=str(e))
                    
                    return enhanced_fields if enhanced_fields else traditional_fields
            except json.JSONDecodeError:
                pass
        
        except Exception as e:
            self.logger.warning("Failed to merge extraction results", error=str(e))
        
        # Fallback to traditional fields
        return traditional_fields
    
    def _enhanced_data_type_mapping(self, data_type_str: str) -> DataType:
        """Enhanced data type mapping with fuzzy matching"""
        if not data_type_str or not isinstance(data_type_str, str):
            return DataType.STRING
        
        data_type_lower = data_type_str.lower().strip()
        
        # Enhanced mapping with more patterns
        type_patterns = {
            DataType.STRING: ['character', 'varchar', 'string', 'text', 'char', 'nvarchar', 'clob'],
            DataType.INTEGER: ['integer', 'int', 'bigint', 'smallint', 'tinyint', 'number'],
            DataType.FLOAT: ['float', 'double', 'decimal', 'numeric', 'real', 'money'],
            DataType.BOOLEAN: ['boolean', 'bool', 'bit', 'flag'],
            DataType.DATE: ['date'],
            DataType.TIMESTAMP: ['timestamp', 'datetime', 'time', 'datetime2'],
            DataType.ARRAY: ['array', 'list', 'collection'],
            DataType.OBJECT: ['object', 'json', 'struct', 'record', 'map']
        }
        
        # Fuzzy matching
        for data_type, patterns in type_patterns.items():
            for pattern in patterns:
                if pattern in data_type_lower or data_type_lower in pattern:
                    return data_type
        
        # Default fallback
        return DataType.STRING
    
    async def _multi_strategy_db_extraction(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Dict[str, Any]:
        """Multi-strategy database name extraction with confidence scoring"""
        
        strategies = [
            ("field_provided_keys", self._extract_from_field_keys),
            ("dictionary_object", self._extract_from_dictionary),
            ("context_patterns", self._extract_from_context_patterns),
            ("ai_analysis", self._extract_using_ai_analysis),
            ("semantic_analysis", self._extract_using_semantic_analysis)
        ]
        
        extraction_results = {}
        confidence_scores = {}
        
        # Try each strategy
        for strategy_name, strategy_func in strategies:
            try:
                result = await strategy_func(document, fields)
                if result and result.get("database_name"):
                    extraction_results[strategy_name] = result
                    confidence_scores[strategy_name] = result.get("confidence", 0.5)
                    self.logger.info(f"Strategy {strategy_name} found: {result['database_name']}")
            except Exception as e:
                self.logger.warning(f"Strategy {strategy_name} failed", error=str(e))
        
        # Consensus analysis
        if extraction_results:
            consensus_result = await self._analyze_extraction_consensus(extraction_results)
            return {
                "database_name": consensus_result["database_name"],
                "confidence": consensus_result["confidence"],
                "notes": consensus_result["notes"],
                "all_strategies": extraction_results,
                "strategy_scores": confidence_scores
            }
        else:
            return {
                "database_name": None,
                "confidence": 0.0,
                "notes": ["No database name could be extracted using any strategy"],
                "all_strategies": {},
                "strategy_scores": {}
            }
    
    async def _extract_from_field_keys(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Optional[Dict[str, Any]]:
        """Extract from field providedKey values"""
        db_candidates = {}
        
        for field in fields:
            if field.provided_key:
                parts = field.provided_key.split('.')
                if len(parts) >= 1:
                    candidate = parts[-1]  # Last part is most likely DB name
                    db_candidates[candidate] = db_candidates.get(candidate, 0) + 1
        
        if db_candidates:
            # Most common candidate
            best_candidate = max(db_candidates.items(), key=lambda x: x[1])
            confidence = min(0.9, best_candidate[1] / len(fields))
            
            return {
                "database_name": best_candidate[0],
                "confidence": confidence,
                "method": "field_keys",
                "supporting_fields": best_candidate[1]
            }
        
        return None
    
    async def _extract_from_dictionary(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Optional[Dict[str, Any]]:
        """Extract from dictionary.providedKey pattern"""
        if 'dictionary' in document:
            dictionary_obj = document['dictionary']
            if isinstance(dictionary_obj, dict) and 'providedKey' in dictionary_obj:
                provided_key = dictionary_obj['providedKey']
                if provided_key:
                    parts = provided_key.split('.')
                    if len(parts) >= 1:
                        return {
                            "database_name": parts[-1],
                            "confidence": 0.85,
                            "method": "dictionary_object",
                            "full_key": provided_key
                        }
        
        return None
    
    async def _extract_from_context_patterns(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Optional[Dict[str, Any]]:
        """Extract using context pattern recognition"""
        def search_recursive(obj, path=""):
            candidates = []
            
            if isinstance(obj, dict):
                # Look for database-related keys
                db_keys = ['database', 'db_name', 'database_name', 'schema', 'catalog']
                for key in db_keys:
                    if key in obj and isinstance(obj[key], str):
                        candidates.append({
                            "name": obj[key],
                            "confidence": 0.8,
                            "source": f"{path}.{key}"
                        })
                
                # Recursive search
                for key, value in obj.items():
                    candidates.extend(search_recursive(value, f"{path}.{key}"))
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    candidates.extend(search_recursive(item, f"{path}[{i}]"))
            
            return candidates
        
        candidates = search_recursive(document)
        
        if candidates:
            # Return highest confidence candidate
            best = max(candidates, key=lambda x: x["confidence"])
            return {
                "database_name": best["name"],
                "confidence": best["confidence"],
                "method": "context_patterns",
                "source": best["source"]
            }
        
        return None
    
    async def _extract_using_ai_analysis(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Optional[Dict[str, Any]]:
        """Use AI to intelligently extract database name"""
        try:
            # Sample of field keys for analysis
            field_keys = [f.provided_key for f in fields if f.provided_key][:10]
            
            messages = [
                {
                    "role": "system",
                    "content": """You are an expert at extracting database names from metadata documents.
                    Analyze the document structure and field patterns to identify the most likely database name.
                    Consider naming conventions, patterns, and context clues.
                    
                    Return ONLY a JSON response with: {"database_name": "name", "confidence": 0.0-1.0, "reasoning": "explanation"}
                    If you cannot determine a database name, return {"database_name": null, "confidence": 0.0, "reasoning": "explanation"}"""
                },
                {
                    "role": "user",
                    "content": f"""
                    Document sample: {json.dumps(dict(list(document.items())[:5]), indent=2)}
                    
                    Field providedKey patterns: {json.dumps(field_keys, indent=2)}
                    
                    What is the most likely database name?
                    """
                }
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=200)
            
            try:
                result = json.loads(response["content"])
                if result.get("database_name"):
                    return {
                        "database_name": result["database_name"],
                        "confidence": result.get("confidence", 0.7),
                        "method": "ai_analysis",
                        "reasoning": result.get("reasoning", "AI analysis")
                    }
            except json.JSONDecodeError:
                pass
                
        except Exception as e:
            self.logger.warning("AI database extraction failed", error=str(e))
        
        return None
    
    async def _extract_using_semantic_analysis(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Optional[Dict[str, Any]]:
        """Use semantic analysis for database name extraction"""
        try:
            # Analyze field names and descriptions for semantic patterns
            semantic_clues = []
            
            for field in fields:
                if field.description:
                    semantic_clues.append(field.description)
                if field.name:
                    semantic_clues.append(field.name)
            
            if semantic_clues:
                messages = [
                    {
                        "role": "system",
                        "content": """Analyze field names and descriptions to infer the database domain/name.
                        Look for semantic patterns like 'customer', 'financial', 'inventory', etc.
                        Return JSON: {"database_name": "inferred_name", "confidence": 0.0-1.0}"""
                    },
                    {
                        "role": "user",
                        "content": f"Field information: {json.dumps(semantic_clues[:20], indent=2)}"
                    }
                ]
                
                response = await self.llm_provider.generate(messages, max_tokens=150)
                
                try:
                    result = json.loads(response["content"])
                    if result.get("database_name"):
                        return {
                            "database_name": result["database_name"],
                            "confidence": result.get("confidence", 0.6),
                            "method": "semantic_analysis",
                            "semantic_clues": len(semantic_clues)
                        }
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            self.logger.warning("Semantic database extraction failed", error=str(e))
        
        return None
    
    async def _analyze_extraction_consensus(
        self, 
        extraction_results: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze consensus among extraction strategies"""
        
        # Count occurrences of each database name
        name_votes = {}
        total_confidence = 0.0
        
        for strategy, result in extraction_results.items():
            db_name = result["database_name"]
            confidence = result.get("confidence", 0.5)
            
            if db_name not in name_votes:
                name_votes[db_name] = {"count": 0, "total_confidence": 0.0, "strategies": []}
            
            name_votes[db_name]["count"] += 1
            name_votes[db_name]["total_confidence"] += confidence
            name_votes[db_name]["strategies"].append(strategy)
            total_confidence += confidence
        
        if not name_votes:
            return {
                "database_name": None,
                "confidence": 0.0,
                "notes": ["No consensus reached"]
            }
        
        # Find consensus winner
        best_candidate = max(name_votes.items(), key=lambda x: (x[1]["count"], x[1]["total_confidence"]))
        winner_name = best_candidate[0]
        winner_data = best_candidate[1]
        
        # Calculate consensus confidence
        consensus_confidence = (
            winner_data["total_confidence"] / winner_data["count"] *  # Average confidence
            (winner_data["count"] / len(extraction_results)) *  # Consensus ratio
            min(1.0, total_confidence / len(extraction_results))  # Overall confidence
        )
        
        notes = [
            f"Consensus reached by {winner_data['count']}/{len(extraction_results)} strategies",
            f"Supporting strategies: {', '.join(winner_data['strategies'])}",
            f"Average confidence: {winner_data['total_confidence'] / winner_data['count']:.2f}"
        ]
        
        if winner_data["count"] == 1:
            notes.append("Warning: Only one strategy found this database name")
        
        return {
            "database_name": winner_name,
            "confidence": consensus_confidence,
            "notes": notes,
            "consensus_details": name_votes
        }
    
    async def _advanced_field_validation(
        self, 
        fields: List[FieldDefinition], 
        context: str,
        validation_rules: List[str]
    ) -> Dict[str, Any]:
        """Advanced field validation with AI assistance"""
        
        overall_result = ValidationResult(is_valid=True)
        field_scores = {}
        total_confidence = 0.0
        
        for field in fields:
            # Traditional validation
            field_result = self._traditional_field_validation(field)
            
            # AI-enhanced validation
            ai_result = await self._ai_field_validation(field, context)
            
            # Merge results
            merged_result = self._merge_validation_results(field_result, ai_result)
            
            if not merged_result.is_valid:
                overall_result.is_valid = False
                overall_result.errors.extend(merged_result.errors)
            
            overall_result.warnings.extend(merged_result.warnings)
            overall_result.suggestions.extend(merged_result.suggestions)
            
            field_scores[field.name] = merged_result.metadata.get("confidence", 0.5)
            total_confidence += field_scores[field.name]
        
        avg_confidence = total_confidence / len(fields) if fields else 0.0
        
        return {
            "result": overall_result,
            "confidence": avg_confidence,
            "field_scores": field_scores
        }
    
    def _traditional_field_validation(self, field: FieldDefinition) -> ValidationResult:
        """Traditional field validation (enhanced from original)"""
        result = ValidationResult(is_valid=True, metadata={"confidence": 0.7})
        
        # Enhanced validation rules
        if not field.name or field.name == 'unknown':
            result.errors.append(f"Field has no valid display name: {field.name}")
            result.is_valid = False
        
        if not field.provided_key:
            result.warnings.append(f"Field '{field.name}' has no providedKey - may cause mapping issues")
        
        if not field.description or len(field.description.strip()) < 10:
            result.warnings.append(f"Field '{field.name}' has insufficient description")
        
        # Data type consistency
        if field.data_type == DataType.STRING and field.format:
            if 'varchar' in field.format.lower():
                try:
                    import re
                    match = re.search(r'varchar\((\d+)\)', field.format.lower())
                    if match:
                        length = int(match.group(1))
                        if length > 4000:
                            result.suggestions.append(
                                f"Consider TEXT type for field '{field.name}' with varchar({length})"
                            )
                        elif length < 10:
                            result.warnings.append(
                                f"Very short varchar({length}) for field '{field.name}' - may truncate data"
                            )
                except:
                    pass
        
        # ProvidedKey validation
        if field.provided_key:
            parts = field.provided_key.split('.')
            if len(parts) < 2:
                result.warnings.append(
                    f"Field '{field.name}' providedKey '{field.provided_key}' seems incomplete - should be 'database.table.field'"
                )
            elif len(parts) > 5:
                result.warnings.append(
                    f"Field '{field.name}' providedKey '{field.provided_key}' seems overly complex"
                )
        
        return result
    
    async def _ai_field_validation(self, field: FieldDefinition, context: str) -> ValidationResult:
        """AI-powered field validation"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """You are an expert database field validator. Analyze the field definition and provide validation feedback.
                    
                    Check for:
                    - Naming conventions and consistency
                    - Data type appropriateness 
                    - Business logic compliance
                    - Potential data quality issues
                    - Integration concerns
                    
                    Return JSON: {
                        "is_valid": true/false,
                        "errors": ["list of errors"],
                        "warnings": ["list of warnings"], 
                        "suggestions": ["list of suggestions"],
                        "confidence": 0.0-1.0
                    }"""
                },
                {
                    "role": "user",
                    "content": f"""
                    Field Definition:
                    {json.dumps(field.dict(), indent=2)}
                    
                    Context:
                    {context[:500]}
                    
                    Please validate this field definition.
                    """
                }
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=300)
            
            try:
                ai_result = json.loads(response["content"])
                return ValidationResult(
                    is_valid=ai_result.get("is_valid", True),
                    errors=ai_result.get("errors", []),
                    warnings=ai_result.get("warnings", []),
                    suggestions=ai_result.get("suggestions", []),
                    metadata={"confidence": ai_result.get("confidence", 0.8), "source": "ai"}
                )
            except json.JSONDecodeError:
                pass
                
        except Exception as e:
            self.logger.warning("AI field validation failed", field_name=field.name, error=str(e))
        
        # Fallback
        return ValidationResult(
            is_valid=True, 
            metadata={"confidence": 0.5, "source": "fallback"}
        )
    
    def _merge_validation_results(
        self, 
        traditional: ValidationResult, 
        ai_result: ValidationResult
    ) -> ValidationResult:
        """Merge traditional and AI validation results"""
        
        merged = ValidationResult(
            is_valid=traditional.is_valid and ai_result.is_valid,
            errors=traditional.errors + ai_result.errors,
            warnings=traditional.warnings + ai_result.warnings,
            suggestions=traditional.suggestions + ai_result.suggestions
        )
        
        # Average confidence scores
        trad_conf = traditional.metadata.get("confidence", 0.5)
        ai_conf = ai_result.metadata.get("confidence", 0.5)
        merged.metadata = {"confidence": (trad_conf + ai_conf) / 2}
        
        return merged
    
    async def _contextual_structure_analysis(
        self, 
        document: Dict[str, Any], 
        context: str
    ) -> Dict[str, Any]:
        """AI-powered contextual document structure analysis"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": """Analyze document structure for metadata validation issues.
                    Look for structural problems, missing metadata, inconsistencies, and improvement opportunities.
                    
                    Return JSON: {
                        "warnings": ["structural warnings"],
                        "suggestions": ["improvement suggestions"],
                        "confidence": 0.0-1.0,
                        "structure_score": 0.0-1.0
                    }"""
                },
                {
                    "role": "user",
                    "content": f"""
                    Document structure: {json.dumps(dict(list(document.items())[:10]), indent=2)}
                    Context: {context[:300]}
                    
                    Analyze for structural issues and improvements.
                    """
                }
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=400)
            
            try:
                analysis = json.loads(response["content"])
                return {
                    "warnings": analysis.get("warnings", []),
                    "suggestions": analysis.get("suggestions", []),
                    "confidence": analysis.get("confidence", 0.7),
                    "structure_score": analysis.get("structure_score", 0.8)
                }
            except json.JSONDecodeError:
                pass
                
        except Exception as e:
            self.logger.warning("Contextual structure analysis failed", error=str(e))
        
        return {
            "warnings": [],
            "suggestions": ["Structure analysis unavailable"],
            "confidence": 0.5,
            "structure_score": 0.7
        }
    
    async def _learn_from_validation(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition], 
        result: ValidationResult
    ):
        """Learn from validation patterns to improve future performance"""
        try:
            # Extract patterns
            patterns = {
                "document_keys": list(document.keys())[:10],
                "field_count": len(fields),
                "field_types": [f.data_type.value for f in fields],
                "common_formats": [f.format for f in fields if f.format],
                "validation_outcome": result.is_valid,
                "error_types": [error[:50] for error in result.errors],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Store in learned patterns
            pattern_key = f"validation_{datetime.utcnow().strftime('%Y%m%d')}"
            if pattern_key not in self.learned_patterns:
                self.learned_patterns[pattern_key] = []
            
            self.learned_patterns[pattern_key].append(patterns)
            
            # Update statistics
            for error in result.errors:
                error_type = error.split(':')[0] if ':' in error else error[:30]
                self.validation_statistics["common_errors"][error_type] = \
                    self.validation_statistics["common_errors"].get(error_type, 0) + 1
            
            # Field pattern analysis
            for field in fields:
                if field.data_type:
                    field_pattern = f"{field.data_type.value}_{field.format or 'no_format'}"
                    self.validation_statistics["field_patterns"][field_pattern] = \
                        self.validation_statistics["field_patterns"].get(field_pattern, 0) + 1
            
            self.logger.info("Learning from validation completed", patterns_stored=len(self.learned_patterns))
            
        except Exception as e:
            self.logger.warning("Failed to learn from validation", error=str(e))
    
    async def _enhanced_schema_validation(
        self, 
        schema: SchemaDefinition, 
        validation_rules: List[str], 
        context: str
    ) -> Dict[str, Any]:
        """Enhanced schema validation (placeholder for future implementation)"""
        # This would implement similar enhancements for schema validation
        # For now, return basic validation
        validation_result = ValidationResult(is_valid=True)
        
        if not schema.name:
            validation_result.errors.append("Schema has no name")
            validation_result.is_valid = False
        
        if not schema.fields:
            validation_result.errors.append("Schema has no fields")
            validation_result.is_valid = False
        
        return {
            "validation_result": validation_result.dict(),
            "schema_name": schema.name,
            "field_count": len(schema.fields),
            "confidence_scores": {"schema_validation": 0.8},
            "enhancement_notes": ["Basic schema validation completed"]
        }