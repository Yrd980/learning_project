package com.ruoyi.complaint.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.complaint.domain.Feedbackresults;
import com.ruoyi.complaint.service.IFeedbackresultsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 投诉处理反馈信息Controller
 * 
 * @author ningf
 * @date 2024-07-15
 */
@RestController
@RequestMapping("/feedbackresults")
public class FeedbackresultsController extends BaseController
{
    @Autowired
    private IFeedbackresultsService feedbackresultsService;

    /**
     * 查询投诉处理反馈信息列表
     */
    @RequiresPermissions("complaint:feedbackresults:list")
    @GetMapping("/list")
    public TableDataInfo list(Feedbackresults feedbackresults)
    {
        startPage();
        List<Feedbackresults> list = feedbackresultsService.selectFeedbackresultsList(feedbackresults);
        return getDataTable(list);
    }

    /**
     * 导出投诉处理反馈信息列表
     */
    @RequiresPermissions("complaint:feedbackresults:export")
    @Log(title = "投诉处理反馈信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Feedbackresults feedbackresults)
    {
        List<Feedbackresults> list = feedbackresultsService.selectFeedbackresultsList(feedbackresults);
        ExcelUtil<Feedbackresults> util = new ExcelUtil<Feedbackresults>(Feedbackresults.class);
        util.exportExcel(response, list, "投诉处理反馈信息数据");
    }

    /**
     * 获取投诉处理反馈信息详细信息
     */
    @RequiresPermissions("complaint:feedbackresults:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(feedbackresultsService.selectFeedbackresultsById(id));
    }

    /**
     * 新增投诉处理反馈信息
     */
    @RequiresPermissions("complaint:feedbackresults:add")
    @Log(title = "投诉处理反馈信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Feedbackresults feedbackresults)
    {
        return toAjax(feedbackresultsService.insertFeedbackresults(feedbackresults));
    }

    /**
     * 修改投诉处理反馈信息
     */
    @RequiresPermissions("complaint:feedbackresults:edit")
    @Log(title = "投诉处理反馈信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Feedbackresults feedbackresults)
    {
        return toAjax(feedbackresultsService.updateFeedbackresults(feedbackresults));
    }

    /**
     * 删除投诉处理反馈信息
     */
    @RequiresPermissions("complaint:feedbackresults:remove")
    @Log(title = "投诉处理反馈信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(feedbackresultsService.deleteFeedbackresultsByIds(ids));
    }
}
