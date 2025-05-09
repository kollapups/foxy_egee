(function($) {
    console.log('task_filter.js loaded at:', new Date().toISOString());
    $(document).ready(function() {
        console.log('jQuery version:', $.fn.jquery);
        console.log('django.jQuery available:', typeof django !== 'undefined' && typeof django.jQuery !== 'undefined');
        
        // Проверка формы
        const $taskForm = $('form[id*="task_form"]');
        console.log('Task form found:', $taskForm.length > 0);
        if (!$taskForm.length) {
            console.error('Task form not found. Check form ID or page context.');
            return;
        }

        // Функция для получения CSRF-токена
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            console.log('CSRF token:', cookieValue || 'Not found');
            return cookieValue;
        }
        const csrftoken = getCookie('csrftoken');

        // Поля формы
        const $subjectField = $('#id_subject');
        const $examPartField = $('#id_exam_part');
        const $examLineField = $('#id_exam_line');
        const $topicField = $('#id_topic');
        const $subtopicField = $('#id_subtopic');
        const $sourceField = $('#id_source');

        console.log('Fields initialized:', {
            subject: $subjectField.length > 0,
            examPart: $examPartField.length > 0,
            examLine: $examLineField.length > 0,
            topic: $topicField.length > 0,
            subtopic: $subtopicField.length > 0,
            source: $sourceField.length > 0
        });

        // Сохраняем начальные значения
        const initialValues = {
            subject: $subjectField.val(),
            examPart: $examPartField.val(),
            examLine: $examLineField.val(),
            topic: $topicField.val(),
            subtopic: $subtopicField.val(),
            source: $sourceField.val()
        };
        console.log('Initial values:', initialValues);

        // Функция для обновления выпадающего списка
        function updateSelect($select, options, selectedValue, defaultText) {
            console.log('Updating select:', $select.attr('id'), 'with options:', options);
            $select.empty();
            $select.append($('<option>').val('').text(defaultText));
            $.each(options, function(index, option) {
                const $option = $('<option>').val(option.id).text(option.name);
                if (option.id == selectedValue) {
                    $option.prop('selected', true);
                }
                $select.append($option);
            });
        }

        // Обработчик изменения subject
        $subjectField.on('change', function() {
            const subject = $(this).val();
            console.log('Subject changed to:', subject);

            if (!subject) {
                console.log('No subject selected, resetting fields');
                updateSelect($examPartField, [], initialValues.examPart, '- Выберите часть -');
                updateSelect($examLineField, [], initialValues.examLine, '- Выберите задание -');
                updateSelect($topicField, [], initialValues.topic, '- Выберите тему -');
                updateSelect($subtopicField, [], initialValues.subtopic, '- Выберите подтему -');
                updateSelect($sourceField, [], initialValues.source, '- Выберите источник -');
                return;
            }

            console.log('Preparing AJAX request to /tasks/get_fields_by_subject/');
            $.ajax({
                url: '/tasks/get_fields_by_subject/', // Попробуйте '/admin/tasks/get_fields_by_subject/' если маршрут в admin
                type: 'GET',
                data: { subject: subject },
                headers: { 'X-CSRFToken': csrftoken },
                beforeSend: function() {
                    console.log('AJAX request starting...');
                },
                success: function(data) {
                    console.log('AJAX success, data:', data);
                    if (data.error) {
                        console.error('Server error:', data.error);
                        return;
                    }
                    updateSelect($examPartField, data.exam_parts, initialValues.examPart, '- Выберите часть -');
                    updateSelect($examLineField, data.exam_lines, initialValues.examLine, '- Выберите задание -');
                    updateSelect($topicField, data.topics, initialValues.topic, '- Выберите тему -');
                    updateSelect($sourceField, data.sources, initialValues.source, '- Выберите источник -');
                    updateSelect($subtopicField, [], initialValues.subtopic, '- Выберите подтему -');
                },
                error: function(xhr, status, error) {
                    console.error('AJAX error:', status, error, xhr.responseText);
                }
            });
        });

        // Обработчик изменения topic
        $topicField.on('change', function() {
            const topicId = $(this).val();
            const subject = $subjectField.val();
            console.log('Topic changed to:', topicId);

            if (!topicId || !subject) {
                console.log('No topic or subject, resetting subtopic');
                updateSelect($subtopicField, [], initialValues.subtopic, '- Выберите подтему -');
                return;
            }

            console.log('Preparing AJAX request to /tasks/get_subtopics/');
            $.ajax({
                url: '/tasks/get_subtopics/', // Попробуйте '/admin/tasks/get_subtopics/' если маршрут в admin
                type: 'GET',
                data: { topic: topicId, subject: subject },
                headers: { 'X-CSRFToken': csrftoken },
                beforeSend: function() {
                    console.log('AJAX request starting for subtopics...');
                },
                success: function(data) {
                    console.log('AJAX success for subtopics, data:', data);
                    if (data.error) {
                        console.error('Server error:', data.error);
                        return;
                    }
                    updateSelect($subtopicField, data.subtopics, initialValues.subtopic, '- Выберите подтему -');
                },
                error: function(xhr, status, error) {
                    console.error('AJAX error for subtopics:', status, error, xhr.responseText);
                }
            });
        });

        // Инициируем при загрузке
        console.log('Checking initial subject:', initialValues.subject);
        if (initialValues.subject) {
            console.log('Triggering initial subject change');
            $subjectField.trigger('change');
            if (initialValues.topic) {
                setTimeout(function() {
                    console.log('Triggering initial topic change');
                    $topicField.trigger('change');
                }, 500);
            }
        }
    });
})(django.jQuery);